#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from typing import List
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from app.memory.schemas import MemorySummary

ReflectPrompt = PromptTemplate(
    template=(
        "Summarize the following memory signals into structured fields:\n"
        "{signals}\n\n"
        "Return JSON with keys: key_signals, best_hint_patterns, common_mistakes, calibration_note."
    ),
    input_variables=["signals"],
)

def build_reflection_chain():
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = ReflectPrompt | llm | RunnableLambda(lambda x: getattr(x, "content", str(x)))
    return chain

def parse_summary(text: str) -> MemorySummary:
    import json
    try:
        start, end = text.find("{"), text.rfind("}")
        payload = json.loads(text[start:end+1])
        return MemorySummary(
            word="",
            key_signals=payload.get("key_signals", []),
            best_hint_patterns=payload.get("best_hint_patterns", []),
            common_mistakes=payload.get("common_mistakes", []),
            calibration_note=payload.get("calibration_note"),
        )
    except Exception:
        return MemorySummary(word="", key_signals=[text])
