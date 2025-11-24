#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from app.agents.hint_agent import build_hint_agent

def test_hint_agent_returns_pydantic(monkeypatch):
    chain = build_hint_agent("huggingface")
    # Override tools to deterministic
    monkeypatch.setattr("app.agents.hint_agent.rag_hint_tool.invoke", lambda args: "RAG: concise hint")
    monkeypatch.setattr("app.agents.hint_agent.compress_hint_tool.invoke", lambda args: args["input"]["text"])
    out = chain.invoke({})
    assert hasattr(out, "hint") and isinstance(out.hint, str)

# backend/tests/test_agents_guess.py
from app.agents.guess_agent import build_guess_agent

def test_guess_agent(monkeypatch):
    chain = build_guess_agent("huggingface")
    out = chain.invoke({"hints": ["disorder increases"]})
    assert hasattr(out, "guess") and hasattr(out, "confidence")

# backend/tests/test_agents_graphs.py
from app.engine.graphs import run_multi_agent_round

def test_multi_agent_flow(monkeypatch):
    # Stabilize agents
    monkeypatch.setattr("app.agents.hint_agent.build_hint_agent",
                        lambda: type("C", (),
                                     {"invoke": lambda self, d: type(
                                         "H", (), {"hint": "concise hint", "rationale": "mock"})()})())
    monkeypatch.setattr("app.agents.guess_agent.build_guess_agent",
                        lambda: type("C", (),
                                     {"invoke": lambda self, d: type(
                                         "G", (), {"guess": "entropy", "confidence": 0.9, "rationale": "mock"})()})())
    monkeypatch.setattr("app.agents.judge_agent.build_judge_agent",
                        lambda: type("C", (),
                                     {"invoke": lambda self, d: type(
                                         "J", (), {"correct": True, "score": 1.0, "feedback": "mock"})()})())
    monkeypatch.setattr("app.evaluation.tool.evaluate_round_tool",
                        type("T", (), {"invoke": lambda self, d: type(
                            "R", (), {"accuracy":1.0,"calibration":0.9,"creativity":0.6,"efficiency":0.7,
                                      "feedback":"ok"})()})())
    
    state = run_multi_agent_round("entropy")
    assert state.hints and state.guesses and state.judgment and state.metrics
