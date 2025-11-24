#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from app.evaluation.metrics import evaluate_round
from app.evaluation.schemas import Guess, RoundEvaluationInput


def test_evaluate_round():
    inp = RoundEvaluationInput(
        target="entropy",
        guesses=[Guess(guess="entropy", confidence=0.9)],
        hints=["disorder increases", "thermodynamics"],
        total_tokens=800,
        total_time_ms=1200,
        steps=3,
    )
    res = evaluate_round(inp)
    assert res.accuracy == 1.0
    assert 0.0 <= res.calibration <= 1.0
    assert 0.0 <= res.creativity <= 1.0
    assert 0.0 <= res.efficiency <= 1.0
    assert isinstance(res.feedback, str)


# backend/tests/test_eval_tool.py
from app.evaluation.tool import evaluate_round_tool, run_evaluation_via_agent


def test_evaluate_round_tool_direct():
    inp = RoundEvaluationInput(
        target="entropy",
        guesses=[Guess(guess="entropy", confidence=0.9)],
        hints=["disorder increases"],
    )
    res = evaluate_round_tool.invoke({"input": inp})
    assert res.accuracy == 1.0


def test_run_evaluation_via_agent_fallback():
    inp = RoundEvaluationInput(
        target="entropy",
        guesses=[Guess(guess="energy", confidence=0.2)],
        hints=["disorder increases"],
        total_tokens=1200,
        total_time_ms=2500,
        steps=4,
    )
    res = run_evaluation_via_agent(inp)
    assert 0.0 <= res.accuracy <= 1.0


# backend/tests/test_eval_exporter.py
from app.evaluation.exporter import to_prometheus_text
from app.evaluation.schemas import RoundEvaluationResult


def test_prometheus_exporter():
    res = RoundEvaluationResult(accuracy=1.0, calibration=0.8, creativity=0.6, efficiency=0.7)
    txt = to_prometheus_text(res, labels={"mode": "heads_up"})
    assert "game_accuracy" in txt and 'mode="heads_up"' in txt
