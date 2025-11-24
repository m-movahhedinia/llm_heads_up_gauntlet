#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.runnables import RunnableLambda
from app.agents.llm_provider import ProviderFactory

def build_orchestrator(provider_name: str):
    llm = ProviderFactory.get_provider(provider_name)
    # Router decides next step: "hint" -> "guess" -> "judge" -> "evaluate"
    router_prompt = PromptTemplate(
        template=(
            "You are the orchestrator. Given the current state summary, choose next action: "
            "'hint', 'guess', 'judge', or 'evaluate'. "
            "Rules: If no hints, start with 'hint'. If hints exist but no guess, 'guess'. "
            "If guess exists and not judged, 'judge'. If judged, 'evaluate'.\n"
            "State: {summary}\nReturn one token (hint|guess|judge|evaluate)."
        ),
        input_variables=["summary"],
    )
    # Post-process to ensure a valid token
    normalize = RunnableLambda(lambda x: x.content.strip().lower().split()[0]
    if hasattr(x, "content") else str(x).strip().lower())
    
    chain = router_prompt | llm | normalize
    return chain
