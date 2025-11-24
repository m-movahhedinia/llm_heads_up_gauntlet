#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from pydantic import BaseModel, Field

class HintOutput(BaseModel):
    hint: str = Field(min_length=1)
    rationale: str | None = None

class GuessOutput(BaseModel):
    guess: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    rationale: str | None = None

class JudgeOutput(BaseModel):
    correct: bool
    score: float = Field(ge=0.0, le=1.0)
    feedback: str | None = None
