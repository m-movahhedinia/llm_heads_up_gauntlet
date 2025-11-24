#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from app.policy.schemas import Policy, PolicyUpdateInput, PolicyUpdateOutput

UpdatePrompt = PromptTemplate(
    template=(
        "You are a policy learner for a word-guessing game.\n"
        "Current policy:\n{policy_json}\n"
        "Metrics: accuracy={accuracy:.2f}, calibration={calibration:.2f}, "
        "creativity={creativity:.2f}, efficiency={efficiency:.2f}\n"
        "Signals:\n{signals}\n\n"
        "Rules:\n"
        "- If accuracy < 1.0, consider increasing retriever_k (<= 5) and max_tokens moderately.\n"
        "- If calibration < 0.6, adjust confidence_bias toward 0 and reduce temperature slightly.\n"
        "- If creativity < 0.5, increase temperature slightly; if efficiency < 0.5, reduce max_tokens or compression_rate↑.\n"
        "- Keep changes small (step size <= 0.1 for continuous, +/-1 for discrete).\n"
        "Return JSON with new_policy and a short rationale."
    ),
    input_variables=["policy_json", "accuracy", "calibration", "creativity", "efficiency", "signals"],
)

def build_policy_learner():
    llm = ChatOpenAI(model="gpt-4o-mini")
    parser = PydanticOutputParser(pydantic_object=PolicyUpdateOutput)
    chain = (
        # Pre-format inputs
        RunnableLambda(lambda x: {
            "policy_json": x["policy"].model_dump_json(),
            "accuracy": x["accuracy"],
            "calibration": x["calibration"],
            "creativity": x["creativity"],
            "efficiency": x["efficiency"],
            "signals": x.get("summary_signals", "") or ""
        })
        | UpdatePrompt
        | llm
        | parser
    )
    return chain

def propose_policy_update(inp: PolicyUpdateInput) -> PolicyUpdateOutput:
    chain = build_policy_learner()
    return chain.invoke(inp)
