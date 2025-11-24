#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from pydantic import BaseModel, Field


class Guess(BaseModel):
    guess: str
    confidence: float = Field(ge=0.0, le=1.0)


class RoundEvaluationInput(BaseModel):
    target: str
    guesses: list[Guess]
    hints: list[str]
    # TODO: Add more metadata to compute efficiency (tokens, time, steps)
    total_tokens: int | None = None
    total_time_ms: int | None = None
    steps: int | None = None


class RoundEvaluationResult(BaseModel):
    accuracy: float = Field(ge=0.0, le=1.0)
    calibration: float = Field(ge=0.0, le=1.0)
    creativity: float = Field(ge=0.0, le=1.0)
    efficiency: float = Field(ge=0.0, le=1.0)
    feedback: str | None = None
