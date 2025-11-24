#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from app.engine.nodes import node_policy_learn
from app.engine.state import RoundState, RoundConfig
from app.core.metrics import ReliabilityMetrics

def test_policy_learn_includes_reliability(monkeypatch):
    s = RoundState(config=RoundConfig(mode="x", word="entropy"))
    class M: accuracy=0.8; calibration=0.5; creativity=0.6; efficiency=0.7
    s.metrics = M()
    s.reliability = ReliabilityMetrics(timeouts=2, retries=3, circuit_opens=1)
    monkeypatch.setattr("app.engine.nodes.update_policy_tool", type("T", (), {"invoke": lambda self, d: type("O", (), {
        "new_policy": type("P", (), {"temperature":0.65,"max_tokens":280,"retriever_k":4,"compression_rate":0.55,"confidence_bias":0.0})(),
        "rationale": "Accounted reliability signals"
    })()})())
    out = node_policy_learn(s)
    assert out.config.top_k == 4
