#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from typing import List
from .schemas import RoundEvaluationInput, RoundEvaluationResult

def compute_accuracy(inp: RoundEvaluationInput) -> float:
    # 1 if any exact match, else 0. Future: semantic equivalence
    return float(any(g.guess.strip().lower() == inp.target.strip().lower() for g in inp.guesses))

def compute_calibration(inp: RoundEvaluationInput) -> float:
    # Simple calibration: confidence of the last guess if correct, 1 - confidence if incorrect
    if not inp.guesses:
        return 0.0
    last = inp.guesses[-1]
    correct = last.guess.strip().lower() == inp.target.strip().lower()
    return float(last.confidence if correct else 1.0 - last.confidence)

def compute_creativity(inp: RoundEvaluationInput) -> float:
    # Proxy: lexical diversity of hints, normalized
    if not inp.hints:
        return 0.0
    unique_tokens = set(" ".join(inp.hints).lower().split())
    denom = sum(len(h.split()) for h in inp.hints)
    if denom == 0:
        return 0.0
    return min(1.0, len(unique_tokens) / max(1, denom))

def compute_efficiency(inp: RoundEvaluationInput) -> float:
    # Normalize by tokens/time/steps if provided; otherwise default mid-score
    base = 0.5
    if inp.total_tokens is not None:
        base += max(0.0, min(0.5, (1000 - min(1000, inp.total_tokens)) / 2000))
    if inp.total_time_ms is not None:
        base += max(0.0, min(0.25, (3000 - min(3000, inp.total_time_ms)) / 12000))
    if inp.steps is not None:
        base += max(0.0, min(0.25, (5 - min(5, inp.steps)) / 20))
    return float(min(1.0, max(0.0, base)))

def aggregate_feedback(inp: RoundEvaluationInput, result: RoundEvaluationResult) -> str:
    lines = []
    lines.append(f"Accuracy: {'correct' if result.accuracy >= 1.0 else 'incorrect'}")
    lines.append(f"Calibration: {result.calibration:.2f} (closer to 1 is better)")
    lines.append(f"Creativity: {result.creativity:.2f} (diverse, concise hints)")
    lines.append(f"Efficiency: {result.efficiency:.2f} (optimized steps/tokens/time)")
    return " | ".join(lines)

def evaluate_round(inp: RoundEvaluationInput) -> RoundEvaluationResult:
    acc = compute_accuracy(inp)
    cal = compute_calibration(inp)
    cre = compute_creativity(inp)
    eff = compute_efficiency(inp)
    res = RoundEvaluationResult(
        accuracy=acc, calibration=cal, creativity=cre, efficiency=eff
    )
    res.feedback = aggregate_feedback(inp, res)
    return res
