#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from app.engine.graphs import run_multi_agent_round_with_learning

def test_policy_integration(monkeypatch):
    # Stabilize upstream nodes
    monkeypatch.setattr("app.engine.graphs.node_orchestrate", lambda s: s)
    monkeypatch.setattr("app.engine.graphs.node_hint_agent", lambda s: s)
    monkeypatch.setattr("app.engine.graphs.node_guess_agent", lambda s: s)
    monkeypatch.setattr("app.engine.graphs.node_judge_agent", lambda s: s)
    # Inject metrics and summary before learner
    def fake_eval(s):
        class M: accuracy=0.9; calibration=0.55; creativity=0.5; efficiency=0.6; feedback="ok"
        s.metrics = M()
        return s
    monkeypatch.setattr("app.engine.graphs.node_evaluate_tool", fake_eval)
    def fake_mem_write(s): return s
    def fake_mem_summary(s):
        class S: key_signals=["signal A"]; best_hint_patterns=["pattern X"]; common_mistakes=["mistake Y"]; calibration_note="note"
        s.memory_summary = S()
        return s
    monkeypatch.setattr("app.engine.graphs.node_memory_write", fake_mem_write)
    monkeypatch.setattr("app.engine.graphs.node_memory_summarize", fake_mem_summary)
    # Deterministic policy update
    monkeypatch.setattr("app.engine.nodes.update_policy_tool", type("T", (), {"invoke": lambda self, d: type("O", (), {
        "new_policy": type("P", (), {"temperature":0.65,"max_tokens":280,"retriever_k":4,"compression_rate":0.55,"confidence_bias":0.0})(),
        "rationale": "Tuned retriever_k and temperature"
    })()})())
    state = run_multi_agent_round_with_learning("entropy")
    assert hasattr(state, "policy")
    assert state.config.top_k == 4
