#!/usr/bin/env python3
"""Author: mansour

Description:

"""

import random

from langchain_core.runnables import RunnableLambda
from llmlingua import PromptCompressor


def build_hint_compressor():
    # TODO Test with various models. Would it work with Phi 4 mini?
    llm_lingua = PromptCompressor()

    def _compress(text: str) -> str:
        out = llm_lingua.compress_prompt([text])
        return out["compressed_text"]

    return RunnableLambda(_compress)


def build_noise_injector(severity: float = 0.1):
    def _noise(text: str) -> str:
        chars = list(text)
        n = max(1, int(len(chars) * severity))
        for _ in range(n):
            idx = random.randint(0, len(chars) - 1)
            chars[idx] = random.choice("xyz!?")
        return "".join(chars)

    return RunnableLambda(_noise)


def build_list_processor(item_runnable: RunnableLambda):
    # Map a runnable over a list of strings
    def _map(items: list[str]) -> list[str]:
        return [item_runnable.invoke(it) for it in items]

    return RunnableLambda(_map)
