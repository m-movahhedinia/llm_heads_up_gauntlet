#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from app.policy.schemas import Policy, PolicyUpdateInput
from app.policy.learner import propose_policy_update

def test_policy_learner_structured(monkeypatch):
    from langchain_core.runnables import RunnableLambda
    # Monkeypatch learner last step to deterministic output
    import app.policy.learner as L
    chain = L.build_policy_learner() | RunnableLambda(lambda _: {
        "new_policy": Policy(temperature=0.6, max_tokens=300, retriever_k=4, compression_rate=0.6, confidence_bias=0.0),
        "rationale": "Improve accuracy and calibration"
    })
    monkeypatch.setattr(L, "build_policy_learner", lambda: chain)
    inp = PolicyUpdateInput(policy=Policy(), accuracy=0.8, calibration=0.5, creativity=0.6, efficiency=0.7)
    out = propose_policy_update(inp)
    assert out.new_policy.retriever_k == 4
    assert "Improve" in out.rationale
