#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MemoryItem(BaseModel):
    # TODO Make this an enum
    kind: str = Field(pattern="^(hint|guess|judge|eval|summary)$")
    content: str
    word: str
    confidence: Optional[float] = None
    correct: Optional[bool] = None
    score: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MemorySummary(BaseModel):
    word: str
    key_signals: List[str] = []
    best_hint_patterns: List[str] = []
    common_mistakes: List[str] = []
    calibration_note: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
