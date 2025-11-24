#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from pydantic import BaseModel, Field
from typing import List, Optional

class Guess(BaseModel):
    guess: str
    confidence: float = Field(ge=0.0, le=1.0)

class RoundEvaluationInput(BaseModel):
    target: str
    guesses: List[Guess]
    hints: List[str]
    # TODO: Add more metadata to compute efficiency (tokens, time, steps)
    total_tokens: Optional[int] = None
    total_time_ms: Optional[int] = None
    steps: Optional[int] = None

class RoundEvaluationResult(BaseModel):
    accuracy: float = Field(ge=0.0, le=1.0)
    calibration: float = Field(ge=0.0, le=1.0)
    creativity: float = Field(ge=0.0, le=1.0)
    efficiency: float = Field(ge=0.0, le=1.0)
    feedback: Optional[str] = None
