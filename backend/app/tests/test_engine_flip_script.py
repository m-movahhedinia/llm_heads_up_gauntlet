#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from app.agents.schemas import GuessOutput, JudgeOutput
from app.engine.graphs import run_flip_script_round


def test_flip_script_flow(monkeypatch):
    def fake_generate_structured(provider, prompt, schema):
        if schema.__name__ == "GuessOutput":
            return GuessOutput(guess="entropy", confidence=0.7, rationale="Likely")
        return JudgeOutput(correct=True, score=0.95, feedback="Close enough")

    monkeypatch.setattr("app.engine.nodes.generate_structured", fake_generate_structured)
    state = run_flip_script_round(word="entropy", provider_name="openai")
    assert state.guesses and state.judgment
    assert state.judgment.correct is True
