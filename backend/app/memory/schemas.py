#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from datetime import datetime

from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    # TODO Make this an enum
    kind: str = Field(pattern="^(hint|guess|judge|eval|summary)$")
    content: str
    word: str
    confidence: float | None = None
    correct: bool | None = None
    score: float | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MemorySummary(BaseModel):
    word: str
    key_signals: list[str] = []
    best_hint_patterns: list[str] = []
    common_mistakes: list[str] = []
    calibration_note: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
