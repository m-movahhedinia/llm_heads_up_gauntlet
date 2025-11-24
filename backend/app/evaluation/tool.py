#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from app.evaluation.metrics import evaluate_round
from app.evaluation.schemas import RoundEvaluationInput, RoundEvaluationResult


@tool
def evaluate_round_tool(input_: RoundEvaluationInput) -> RoundEvaluationResult:
    """Evaluate a game round for accuracy, calibration, creativity, and efficiency."""
    return evaluate_round(input_)


def build_evaluator_agent():
    llm = ChatOpenAI(model="gpt-4o-mini")
    # The agent is instructed to call the tool when asked to evaluate
    system = PromptTemplate(
        template=(
            "You are an evaluation assistant. When asked to assess a round, "
            "use the available tool to compute metrics. If the user provides target, "
            "guesses, hints, and optional token/time/steps, call the tool."
        ),
        input_variables=[],
    )
    # Compose LCEL: system prompt -> llm with tools
    agent = system | llm.bind_tools([evaluate_round_tool])
    return agent


def run_evaluation_via_agent(inp: RoundEvaluationInput) -> RoundEvaluationResult:
    agent = build_evaluator_agent()
    # In LCEL, the LLM will emit a tool call argument; LangChain handles tool resolution automatically
    result = agent.invoke({})
    # If the model doesn't proactively call, we can directly call the tool:
    # But typically, you'd pass a user prompt; here we ensure deterministic evaluation via direct tool call.
    # For practical usage, provide a user message:
    user_prompt = (
        "Evaluate the round using the tool. "
        f"Target: {inp.target}. "
        f"Guesses: {[g.model_dump() for g in inp.guesses]}. "
        f"Hints: {inp.hints}. "
        f"Tokens: {inp.total_tokens}, Time: {inp.total_time_ms}ms, Steps: {inp.steps}."
    )
    # Re-run with user prompt so the LLM calls the tool:
    result = agent.invoke({"input": user_prompt})
    # Tool return is already a RoundEvaluationResult object when tool is called.
    # For safety, if it's text, fall back to direct call.
    if isinstance(result, RoundEvaluationResult):
        return result
    if hasattr(result, "additional_kwargs") and "tool_calls" in result.additional_kwargs:
        # Tool result should have been captured; however, depending on client version,
        # you might need to wire ToolNode in LangGraph. Fallback:
        return evaluate_round(inp)
    # Fallback to direct computation
    return evaluate_round(inp)
