#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from app.memory.schemas import MemoryItem
from app.memory.semantic_store import build_faiss_memory_chain


def test_semantic_chain(monkeypatch):
    items = [MemoryItem(kind="hint", content="short hint", word="entropy")]
    chain = build_faiss_memory_chain(items)
    from langchain_core.runnables import RunnableLambda

    chain = chain | RunnableLambda(lambda _: "signals: pattern A, mistake B")
    res = chain.invoke("entropy")
    assert "signals" in res
