#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
import pytest
from app.engine.graphs import build_multi_agent_graph_with_memory
from app.engine.state import RoundState, RoundConfig

@pytest.mark.asyncio
async def test_graph_memory_flow(monkeypatch):
    # Stabilize agents and memory nodes for deterministic test
    from app.engine.graphs import node_orchestrate, node_hint_agent, node_guess_agent, node_judge_agent, node_evaluate_tool
    monkeypatch.setattr("app.engine.graphs.node_orchestrate", lambda s: s)
    monkeypatch.setattr("app.engine.graphs.node_hint_agent", lambda s: s)
    monkeypatch.setattr("app.engine.graphs.node_guess_agent", lambda s: s)
    monkeypatch.setattr("app.engine.graphs.node_judge_agent", lambda s: s)
    monkeypatch.setattr("app.engine.graphs.node_evaluate_tool", lambda s: s)
    state = RoundState(config=RoundConfig(mode="multi_agent_mem", word="entropy"))
    app = build_multi_agent_graph_with_memory().compile()
    out = app.invoke(state)
    assert hasattr(out, "logs")
