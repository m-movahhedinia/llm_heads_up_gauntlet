#!/usr/bin/env python3
"""Author: mansour

Description:

Example:
state = run_heads_up_round_with_eval("entropy")
print(state.metrics.dict())
# {
#   "accuracy": 1.0,
#   "calibration": 0.9,
#   "creativity": 0.6,
#   "efficiency": 0.7,
#   "feedback": "Accuracy: correct | Calibration: 0.90 ..."
# }
"""

from langgraph.graph import END, StateGraph

from app.agents.guess_agent import build_guess_agent
from app.agents.hint_agent import build_hint_agent
from app.agents.judge_agent import build_judge_agent
from app.agents.orchestrator import build_orchestrator
from app.engine.nodes import (
    build_guess_chain,
    build_hint_chain,
    build_judge_chain,
    node_compress,
    node_compress_hints,
    node_guess_agent,
    node_hint_agent,
    node_inject_noise,
    node_judge_agent,
    node_memory_read_for_hint,
    node_memory_summarize,
    node_memory_write,
    node_policy_learn,
    node_rag_hint,
)
from app.engine.state import GameMode, RoundConfig, RoundState
from app.evaluation.exporter import to_prometheus_text
from app.evaluation.metrics import evaluate_round
from app.evaluation.schemas import Guess, RoundEvaluationInput
from app.evaluation.tool import evaluate_round_tool


def node_evaluate(state):
    # TODO Wire into graphs
    # Wire into heads-up graph:
    # graph.add_node("evaluate", node_evaluate)
    # graph.add_edge("judge", "evaluate")
    # graph.add_edge("evaluate", END)
    inp = RoundEvaluationInput(
        target=state.config.word,
        guesses=state.guesses,
        hints=[h.hint for h in state.hints],
        total_tokens=None,  # populate if tracked
        total_time_ms=None,
        steps=len(state.logs) if state.logs else None,
    )
    inp = RoundEvaluationInput.model_validate(inp)
    # Call the tool directly (function‑calling style)
    res = evaluate_round(inp)
    state.logs.append(f"Evaluation: {res.feedback}")
    # Export to Prometheus format (save to file or push gateway)
    payload = to_prometheus_text(res, labels={"mode": state.config.mode})
    state.logs.append(f"Metrics:\n{payload}")
    return state


# TODO Move to nodes.py
def node_hint(state: RoundState) -> RoundState:
    chain = build_hint_chain(state.config)
    hint = chain.invoke({"word": state.config.word})
    state.hints.append(hint)
    state.logs.append(f"Hint: {hint.hint}")
    return state


def node_guess(state: RoundState) -> RoundState:
    chain = build_guess_chain(state.config)
    guess = chain.invoke({"hints": [h.hint for h in state.hints]})
    state.guesses.append(guess)
    state.logs.append(f"Guess: {guess.guess}")
    return state


def node_judge(state: RoundState) -> RoundState:
    chain = build_judge_chain(state.config)
    latest = state.guesses[-1]
    judgment = chain.invoke({"word": state.config.word, "guess": latest.guess})
    state.judgment = judgment
    state.logs.append(f"Judged: correct={judgment.correct}, score={judgment.score}")
    return state


def build_heads_up_graph() -> StateGraph:
    graph = StateGraph(RoundState)
    graph.add_node("hint", node_hint)
    graph.add_node("guess", node_guess)
    graph.add_node("judge", node_judge)

    graph.set_entry_point("hint")
    graph.add_edge("hint", "guess")
    graph.add_edge("guess", "judge")
    graph.add_edge("judge", END)
    return graph


def build_heads_up_graph_v2_experimental() -> StateGraph:
    graph = StateGraph(RoundState)
    graph.add_node("hint", node_hint)
    graph.add_node("compress", node_compress)
    graph.add_node("guess", node_guess)
    graph.add_node("judge", node_judge)

    graph.set_entry_point("hint")
    graph.add_edge("hint", "compress")
    graph.add_edge("compress", "guess")
    graph.add_edge("guess", "judge")
    graph.add_edge("judge", END)

    return graph


def build_flip_script_graph() -> StateGraph:
    graph = StateGraph(RoundState)
    # In flip-script, the reference model guesses with minimal context (word category, etc.)
    graph.add_node("guess", node_guess)
    graph.add_node("judge", node_judge)

    graph.set_entry_point("guess")
    graph.add_edge("guess", "judge")
    graph.add_edge("judge", END)
    return graph


def run_heads_up_round(word: str, provider_name: str = "openai", compress_hints: bool = True) -> RoundState:
    cfg = RoundConfig(mode=GameMode.HEADS_UP, word=word, provider_name=provider_name, compress_hints=compress_hints)
    state = RoundState(config=cfg)
    app = build_heads_up_graph().compile()
    return app.invoke(state)


def run_flip_script_round(word: str, provider_name: str = "openai") -> RoundState:
    cfg = RoundConfig(mode=GameMode.FLIP_SCRIPT, word=word, provider_name=provider_name)
    state = RoundState(config=cfg)
    app = build_flip_script_graph().compile()
    return app.invoke(state)


def build_heads_up_graph_with_rag() -> StateGraph:
    graph = StateGraph(RoundState)
    graph.add_node("rag_hint", node_rag_hint)
    graph.add_node("compress", node_compress_hints)
    graph.add_node("noise", node_inject_noise)
    graph.add_node("guess", node_guess)
    graph.add_node("judge", node_judge)

    graph.set_entry_point("rag_hint")
    graph.add_edge("rag_hint", "compress")
    graph.add_edge("compress", "noise")
    graph.add_edge("noise", "guess")
    graph.add_edge("guess", "judge")
    graph.add_edge("judge", END)
    return graph


def build_heads_up_graph_with_eval() -> StateGraph:
    graph = StateGraph(RoundState)
    graph.add_node("rag_hint", node_rag_hint)
    graph.add_node("compress", node_compress_hints)
    graph.add_node("noise", node_inject_noise)
    graph.add_node("guess", node_guess)
    graph.add_node("judge", node_judge)
    graph.add_node("evaluate", node_evaluate)

    graph.set_entry_point("rag_hint")
    graph.add_edge("rag_hint", "compress")
    graph.add_edge("compress", "noise")
    graph.add_edge("noise", "guess")
    graph.add_edge("guess", "judge")
    graph.add_edge("judge", "evaluate")
    graph.add_edge("evaluate", END)
    return graph


def run_heads_up_round_with_eval(word: str, provider_name: str = "openai") -> RoundState:
    cfg = RoundConfig(mode="heads_up", word=word, provider_name=provider_name, compress_hints=True)
    state = RoundState(config=cfg)
    app = build_heads_up_graph_with_eval().compile()
    return app.invoke(state)


def build_flip_script_graph_with_eval() -> StateGraph:
    graph = StateGraph(RoundState)
    graph.add_node("guess", node_guess)
    graph.add_node("judge", node_judge)
    graph.add_node("evaluate", node_evaluate)

    graph.set_entry_point("guess")
    graph.add_edge("guess", "judge")
    graph.add_edge("judge", "evaluate")
    graph.add_edge("evaluate", END)
    return graph


def run_flip_script_round_with_eval(word: str, provider_name: str = "openai") -> RoundState:
    cfg = RoundConfig(mode="flip_script", word=word, provider_name=provider_name)
    state = RoundState(config=cfg)
    app = build_flip_script_graph_with_eval().compile()
    return app.invoke(state)


def run_heads_up_round_with_rag(word: str, provider_name: str = "openai") -> RoundState:
    # Reuse existing RoundConfig/RoundState from Phase 5
    from app.engine.state import RoundConfig

    cfg = RoundConfig(mode=GameMode.HEADS_UP, word=word, provider_name=provider_name, compress_hints=True)
    state = RoundState(config=cfg)
    app = build_heads_up_graph_with_rag().compile()
    return app.invoke(state)


# TODO: Move to these to another file. Maybe orchestration.py
def _summarize_state(state: RoundState) -> str:
    return f"hints={len(state.hints)} guesses={len(state.guesses)} judged={'yes' if state.judgment else 'no'}"


def node_orchestrate(state: RoundState) -> RoundState:
    router = build_orchestrator()
    decision = router.invoke({"summary": _summarize_state(state)})
    state.logs.append(f"Orchestrator: {decision}")
    # TODO This line is deprecated. Add its own enum
    state.config.mode = f"agent:{decision}"
    return state


def node_hint_agent(state: RoundState) -> RoundState:
    chain = build_hint_agent(state.config.provider_name)
    out = chain.invoke({})
    state.hints.append(out)
    state.logs.append(f"Hint agent: {out.hint}")
    return state


def node_guess_agent(state: RoundState) -> RoundState:
    chain = build_guess_agent(state.config.provider_name)
    out = chain.invoke({"hints": [h.hint for h in state.hints]})
    state.guesses.append(out)
    state.logs.append(f"Guess agent: {out.guess} ({out.confidence:.2f})")
    return state


def node_judge_agent(state: RoundState) -> RoundState:
    chain = build_judge_agent(state.config.provider_name)
    latest = state.guesses[-1]
    out = chain.invoke({"word": state.config.word, "guess": latest.guess})
    state.judgment = out
    state.logs.append(f"Judge agent: correct={out.correct} score={out.score:.2f}")
    return state


def node_evaluate_tool(state: RoundState) -> RoundState:
    inp = RoundEvaluationInput(
        target=state.config.word,
        guesses=[Guess(guess=g.guess, confidence=g.confidence) for g in state.guesses],
        hints=[h.hint for h in state.hints],
        steps=len(state.logs),
    )
    inp = RoundEvaluationInput.model_validate(inp)
    res = evaluate_round_tool.invoke({"input": inp})
    state.metrics = res
    state.logs.append(f"Evaluate tool: {res.feedback}")
    return state


def build_multi_agent_graph() -> StateGraph:
    graph = StateGraph(RoundState)
    graph.add_node("orchestrate", node_orchestrate)
    graph.add_node("hint", node_hint_agent)
    graph.add_node("guess", node_guess_agent)
    graph.add_node("judge", node_judge_agent)
    graph.add_node("evaluate", node_evaluate_tool)

    graph.set_entry_point("orchestrate")
    # Decision edges: we re-enter orchestrate unless terminal
    graph.add_edge("orchestrate", "hint")
    graph.add_edge("orchestrate", "guess")
    graph.add_edge("orchestrate", "judge")
    graph.add_edge("orchestrate", "evaluate")

    # After each agent step, go back to orchestrate (except after evaluate → END)
    graph.add_edge("hint", "orchestrate")
    graph.add_edge("guess", "orchestrate")
    graph.add_edge("judge", "orchestrate")
    graph.add_edge("evaluate", END)
    return graph


def run_multi_agent_round(word: str, provider_name: str = "openai") -> RoundState:
    # TODO This line is deprecated. Add its own enum
    cfg = RoundConfig(mode="multi_agent", word=word, provider_name=provider_name, compress_hints=True)
    state = RoundState(config=cfg)
    app = build_multi_agent_graph().compile()
    return app.invoke(state)


def build_multi_agent_graph_with_memory() -> StateGraph:
    graph = StateGraph(RoundState)
    graph.add_node("orchestrate", node_orchestrate)
    graph.add_node("hint_mem", node_memory_read_for_hint)
    graph.add_node("hint", node_hint_agent)
    graph.add_node("guess", node_guess_agent)
    graph.add_node("judge", node_judge_agent)
    graph.add_node("evaluate", node_evaluate_tool)
    graph.add_node("mem_write", node_memory_write)
    graph.add_node("mem_summary", node_memory_summarize)

    graph.set_entry_point("orchestrate")
    graph.add_edge("orchestrate", "hint_mem")
    graph.add_edge("hint_mem", "hint")
    graph.add_edge("orchestrate", "guess")
    graph.add_edge("orchestrate", "judge")
    graph.add_edge("orchestrate", "evaluate")
    graph.add_edge("evaluate", "mem_write")
    graph.add_edge("mem_write", "mem_summary")
    graph.add_edge("mem_summary", END)
    # If not evaluated, still write memory at end of judge
    graph.add_edge("judge", "mem_write")
    return graph


async def run_multi_agent_round_with_memory(word: str, provider_name: str = "openai") -> RoundState:
    state = RoundState(config=RoundConfig(mode="multi_agent_mem", word=word, provider_name=provider_name))
    app = build_multi_agent_graph_with_memory().compile()
    return app.invoke(state)


def build_multi_agent_graph_with_learning() -> StateGraph:
    graph = StateGraph(RoundState)
    graph.add_node("orchestrate", node_orchestrate)
    graph.add_node("hint", node_hint_agent)
    graph.add_node("guess", node_guess_agent)
    graph.add_node("judge", node_judge_agent)
    graph.add_node("evaluate", node_evaluate_tool)
    graph.add_node("mem_write", node_memory_write)
    graph.add_node("mem_summary", node_memory_summarize)
    graph.add_node("policy_learn", node_policy_learn)

    graph.set_entry_point("orchestrate")
    graph.add_edge("orchestrate", "hint")
    graph.add_edge("hint", "guess")
    graph.add_edge("guess", "judge")
    graph.add_edge("judge", "evaluate")
    graph.add_edge("evaluate", "mem_write")
    graph.add_edge("mem_write", "mem_summary")
    graph.add_edge("mem_summary", "policy_learn")
    graph.add_edge("policy_learn", END)
    return graph


def run_multi_agent_round_with_learning(word: str, provider_name: str = "openai") -> RoundState:
    from app.engine.state import RoundConfig

    state = RoundState(config=RoundConfig(mode="multi_agent_learn", word=word, provider_name=provider_name))
    app = build_multi_agent_graph_with_learning().compile()
    return app.invoke(state)
