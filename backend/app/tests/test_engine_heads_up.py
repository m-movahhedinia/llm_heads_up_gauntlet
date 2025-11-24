#!/usr/bin/env python3
"""Author: mansour

Description:

"""

import pytest

from app.engine.graphs import run_heads_up_round


class FakeHint:
    hint = "It increases disorder"
    rationale = "Thermodynamics"


class FakeGuess:
    guess = "entropy"
    confidence = 0.9
    rationale = "Matches hint"


class FakeJudge:
    correct = True
    score = 1.0
    feedback = "Exact match"


@pytest.mark.usefixtures()
def test_heads_up_flow(monkeypatch):
    def fake_generate_structured(provider, prompt, schema):
        name = schema.__name__
        if name == "HintOutput":
            return FakeHint()
        if name == "GuessOutput":
            return FakeGuess()
        if name == "JudgeOutput":
            return FakeJudge()
        raise ValueError("Unknown schema")

    monkeypatch.setattr("app.engine.nodes.generate_structured", fake_generate_structured)
    state = run_heads_up_round(word="entropy", provider_name="openai", compress_hints=False)
    assert state.hints and state.guesses and state.judgment
    assert state.judgment.correct is True
    assert state.guesses[-1].guess == "entropy"
