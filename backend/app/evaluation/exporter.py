#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from app.evaluation.schemas import RoundEvaluationResult


def to_prometheus_text(res: RoundEvaluationResult, labels: dict[str, str] | None = None) -> str:
    labels = labels or {}
    label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])

    def line(name: str, value: float) -> str:
        return f"{name}{{{label_str}}} {value}"

    lines = [
        line("game_accuracy", res.accuracy),
        line("game_calibration", res.calibration),
        line("game_creativity", res.creativity),
        line("game_efficiency", res.efficiency),
    ]
    return "\n".join(lines) + "\n"
