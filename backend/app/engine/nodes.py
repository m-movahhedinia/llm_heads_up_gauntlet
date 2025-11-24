#!/usr/bin/env python3
"""
Author: mansour

Description:

"""

from typing import List
from loguru import logger
from app.engine.state import RoundState, RoundConfig
from app.agents.llm_provider import ProviderFactory, generate_structured
from app.agents.schemas import HintOutput, GuessOutput, JudgeOutput
from app.core.config import settings
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts.prompt import PromptTemplate
from app.knowledge.rag import build_faiss_rag_hint_chain
from app.knowledge.processors import build_hint_compressor, build_noise_injector, build_list_processor
from app.engine.state import RoundState
from app.memory.episodic_store import write_item, read_items
from app.memory.semantic_store import build_faiss_memory_chain
from app.memory.reflect import build_reflection_chain, parse_summary
from app.memory.schemas import MemoryItem, MemorySummary
from app.agents.schemas import HintOutput, GuessOutput, JudgeOutput
from app.core.reliability import with_timeout, with_retry, CircuitBreaker, with_circuit_breaker
from app.core.tokens import TokenBudget
from app.core.validation import SafeGenParams
from app.agents.hint_agent import build_hint_agent
from app.agents.guess_agent import build_guess_agent
from app.agents.judge_agent import build_judge_agent
from app.core.metrics import ReliabilityMetrics
from app.engine.state import RoundState
from app.policy.schemas import Policy, PolicyUpdateInput
from app.policy.tools import update_policy_tool
from app.core.metrics import ReliabilityMetrics
from app.engine.state import RoundState
from app.policy.schemas import Policy, PolicyUpdateInput
from app.policy.tools import update_policy_tool
from app.engine.instrumentation import instrument_guarded
from app.obs.metrics import rounds_total

# TODO move compression to LLMLingua 2
try:
    from llmlingua import LLMLingua
    _LINGUA_AVAILABLE = True
except Exception:
    _LINGUA_AVAILABLE = False

def build_hint_chain(cfg: RoundConfig):
    llm = ProviderFactory.get_provider(cfg.provider_name)
    parser = PydanticOutputParser(pydantic_object=HintOutput)
    prompt = PromptTemplate(
        # TODO This is a debug template, replace with a proper jinja2 template
        template="Give a concise hint for the word '{word}'.\n{format_instructions}",
        input_variables=["word"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt | llm | parser


def build_guess_chain(cfg: RoundConfig):
    llm = ProviderFactory.get_provider(cfg.provider_name)
    parser = PydanticOutputParser(pydantic_object=GuessOutput)
    prompt = PromptTemplate(
        # TODO This is a debug template, replace with a proper jinja2 template
        template="Based on these hints: {hints}\nGuess the word.\n{format_instructions}",
        input_variables=["hints"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt | llm | parser


def build_judge_chain(cfg: RoundConfig):
    llm = ProviderFactory.get_provider(cfg.provider_name)
    parser = PydanticOutputParser(pydantic_object=JudgeOutput)
    prompt = PromptTemplate(
        # TODO This is a debug template, replace with a proper jinja2 template
        template="Target word: {word}\nGuess: {guess}\nJudge correctness and score.\n{format_instructions}",
        input_variables=["word", "guess"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt | llm | parser


def node_compress(state: RoundState) -> RoundState:
    if not state.hints:
        return state
    if (not state.config.compress_hints or not _LINGUA_AVAILABLE) and settings.compress_prompts:
        # Fall back to original hints
        state.compressed_hints = [h.hint for h in state.hints]
        state.logs.append("Compression skipped or LLMLingua unavailable.")
        return state
    compressor = LLMLingua()
    compressed: List[str] = []
    for h in state.hints:
        # LLMLingua expects text, returns compressed text
        out = compressor.compress_text(
            h.hint,
            rate=0.5,              # default compression rate; tune later
            force_tokens=[],       # reserved tokens if needed
        )
        compressed.append(out["compressed_text"])
    state.compressed_hints = compressed
    state.logs.append("Hints compressed via LLMLingua.")
    return state


def node_rag_hint(state: RoundState, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2") -> RoundState:
    # TODO Consider building a vector store from a bootstrap texts
    chain = build_faiss_rag_hint_chain(embedding_model)
    hint_text = chain.invoke(state.config.word)
    state.hints.append(HintOutput(hint=hint_text, rationale="RAG"))
    state.logs.append(f"RAG hint: {hint_text}")
    return state

def node_compress_hints(state: RoundState) -> RoundState:
    if not state.hints:
        return state
    hints = [h.hint for h in state.hints]
    compressor = build_hint_compressor()
    list_proc = build_list_processor(compressor)
    compressed = list_proc.invoke(hints)
    state.compressed_hints = compressed
    state.logs.append("Hints compressed via LLMLingua.")
    return state

def node_inject_noise(state: RoundState) -> RoundState:
    if not state.compressed_hints:
        return state
    noise = build_noise_injector(severity=0.1)
    list_proc = build_list_processor(noise)
    noisy = list_proc.invoke(state.compressed_hints)
    state.compressed_hints = noisy
    state.logs.append("Noise injected into compressed hints.")
    return state

async def node_memory_write(state: RoundState) -> RoundState:
    # Write hint/guess/judge to episodic memory
    for h in state.hints:
        await write_item(MemoryItem(kind="hint", content=h.hint, word=state.config.word))
    for g in state.guesses:
        await write_item(MemoryItem(kind="guess", content=g.guess, word=state.config.word, confidence=g.confidence))
    if state.judgment:
        await write_item(MemoryItem(kind="judge", content=state.judgment.feedback or "", word=state.config.word, correct=state.judgment.correct, score=state.judgment.score))
    state.logs.append("Wrote items to episodic memory.")
    return state

async def node_memory_summarize(state: RoundState) -> RoundState:
    items = await read_items(state.config.word)
    chain = build_faiss_memory_chain(items)
    signals = chain.invoke(state.config.word)
    reflect = build_reflection_chain()
    summary_text = reflect.invoke({"signals": signals})
    summary = parse_summary(summary_text)
    summary.word = state.config.word
    # Attach to state and write as summary
    state.memory_summary = summary
    await write_item(MemoryItem(kind="summary", content=signals, word=state.config.word))
    state.logs.append("Updated semantic memory summary.")
    return state

def node_memory_read_for_hint(state: RoundState) -> RoundState:
    # Use summary to prepend patterns to hint agent context
    s = getattr(state, "memory_summary", None)
    if s and s.best_hint_patterns:
        state.logs.append(f"Memory patterns for hint: {s.best_hint_patterns[:2]}")
    return state

breaker = CircuitBreaker(fail_threshold=3, cool_down=10.0)

def guarded(chain):
    return with_circuit_breaker(with_retry(with_timeout(chain, seconds=25), attempts=2), breaker)

def node_hint_agent(state):
    # params = SafeGenParams(temperature=state.config.temperature, top_k=state.config.top_k,
    #                        max_tokens=state.config.max_tokens)
    # chain = guarded(build_hint_agent())
    # out = chain.invoke({})
    # state.hints.append(out)
    # state.logs.append(f"Hint agent (guarded): {out.hint}")
    # return state
    rounds_total.labels(mode=state.config.mode).inc()
    chain = instrument_guarded("hint", build_hint_agent())
    out = chain.invoke({})
    state.hints.append(out)
    state.logs.append(f"Hint agent: {out.hint}")
    return state

def node_guess_agent(state):
    chain = guarded(build_guess_agent())
    out = chain.invoke({"hints": [h.hint for h in state.hints]})
    state.guesses.append(out)
    state.logs.append(f"Guess agent (guarded): {out.guess}")
    return state

def node_judge_agent(state):
    chain = guarded(build_judge_agent())
    latest = state.guesses[-1]
    out = chain.invoke({"word": state.config.word, "guess": latest.guess})
    state.judgment = out
    state.logs.append(f"Judge agent (guarded): correct={out.correct} score={out.score:.2f}")
    return state

def node_policy_learn(state: RoundState) -> RoundState:
    """
    Apply LCEL-based policy learner updates after evaluation and memory summarization.
    Requires:
      - state.metrics (from evaluation node)
      - optional state.memory_summary (from memory summarization)
      - optional state.reliability (timeouts/retries/circuit-open counters)
    Produces:
      - state.policy (Policy snapshot)
      - updates in state.config: temperature, max_tokens, top_k
      - log entry with rationale
    """
    # Ensure we have metrics to learn from
    metrics = getattr(state, "metrics", None)
    if metrics is None:
        state.logs.append("Policy learner skipped (no metrics present).")
        return state

    # Current runtime policy derived from config
    current = Policy(
        temperature=float(getattr(state.config, "temperature", 0.7)),
        max_tokens=int(getattr(state.config, "max_tokens", 256)),
        retriever_k=int(getattr(state.config, "top_k", 3)),
        compression_rate=0.5,   # If you persist compression elsewhere, pull it in here
        confidence_bias=0.0
    )

    # Reliability signals (optional; used to inform learner)
    rel: ReliabilityMetrics = getattr(state, "reliability", ReliabilityMetrics())

    # Memory summary signals (optional; enrich learner context)
    summary = getattr(state, "memory_summary", None)
    summary_signals = ""
    if summary:
        try:
            summary_signals = ", ".join(
                (summary.key_signals or [])
                + (summary.best_hint_patterns or [])
                + (summary.common_mistakes or [])
            )
            if getattr(summary, "calibration_note", None):
                summary_signals += f", {summary.calibration_note}"
        except Exception:
            # Defensive: never break learner due to summary structure
            summary_signals = str(summary)

    # Append reliability counters to signals
    summary_signals = (summary_signals or "")
    summary_signals += (
        f" | timeouts={rel.timeouts}, retries={rel.retries}, circuit_opens={rel.circuit_opens}"
    )

    # Build learner input
    inp = PolicyUpdateInput(
        policy=current,
        accuracy=float(metrics.accuracy),
        calibration=float(metrics.calibration),
        creativity=float(metrics.creativity),
        efficiency=float(metrics.efficiency),
        summary_signals=summary_signals,
    )

    # Invoke LCEL tool (function calling under the hood)
    out = update_policy_tool.invoke({"input": inp})

    # Apply bounded updates to runtime config
    np = out.new_policy
    # Clamp values to safe ranges
    new_temperature = float(max(0.0, min(2.0, np.temperature)))
    new_max_tokens = int(max(32, min(4096, np.max_tokens)))
    new_top_k = int(max(1, min(20, np.retriever_k)))

    # Update RoundState config
    state.config.temperature = new_temperature
    state.config.max_tokens = new_max_tokens
    state.config.top_k = new_top_k

    # Persist full policy snapshot for observability
    state.policy = np

    # Log rationale
    state.logs.append(
        f"Policy updated: temp={new_temperature}, max_tokens={new_max_tokens}, top_k={new_top_k} | {out.rationale}"
    )

    return state

