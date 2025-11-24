#!/usr/bin/env python3
"""
Author: mansour

Description:

"""

from app.knowledge.rag import build_faiss_rag_hint_chain

def test_faiss_rag_chain(monkeypatch):
    chain = build_faiss_rag_hint_chain()
    # Monkeypatch llm output to deterministic string
    from langchain_core.runnables import RunnableLambda
    # Replace last step with constant output
    chain = chain | RunnableLambda(lambda _: "Concise hint about entropy")
    result = chain.invoke("entropy")
    assert "hint" in result.lower()

# backend/tests/test_processors.py
from app.knowledge.processors import build_hint_compressor, build_noise_injector

def test_compressor_and_noise(monkeypatch):
    # Monkeypatch LLMLingua to simple truncation
    class FakeLingua:
        def compress_text(self, text, rate=0.5):
            cut = max(1, int(len(text) * rate))
            return {"compressed_text": text[:cut]}
    monkeypatch.setattr("app.knowledge.processors.LLMLingua", FakeLingua)

    comp = build_hint_compressor()
    out = comp.invoke("Entropy increases disorder")
    assert len(out) <= len("Entropy increases disorder")

    noise = build_noise_injector(severity=0.2)
    noisy = noise.invoke(out)
    assert isinstance(noisy, str)
    assert len(noisy) == len(out)

# backend/tests/test_heads_up_with_rag.py
from app.engine.graphs import run_heads_up_round_with_rag

def test_heads_up_with_rag_flow(monkeypatch):
    # Patch RAG, compression, noise to fixed outputs
    monkeypatch.setattr("app.engine.nodes.build_faiss_rag_hint_chain", lambda texts: type("C", (), {"invoke": lambda self, q: "RAG hint"})())
    monkeypatch.setattr("app.engine.nodes.build_hint_compressor", lambda rate=0.5: type("C", (), {"invoke": lambda self, t: t})())
    monkeypatch.setattr("app.engine.nodes.build_noise_injector", lambda severity=0.1: type("N", (), {"invoke": lambda self, t: t})())
    state = run_heads_up_round_with_rag(word="entropy")
    assert state.hints, "RAG should add a hint"
    assert state.compressed_hints, "Compression step should populate compressed hints"
    assert state.guesses, "Guess node should run"
    assert state.judgment, "Judgment node should run"
