#!/usr/bin/env python3
"""
Author: mansour

Description:

"""

from sqlmodel import SQLModel, Field
from typing import Optional

class WordDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str

class RoundDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word_id: int = Field(foreign_key="worddb.id")
    correct: bool
    hints_used: int
    score: float

class LeaderboardDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participant: str
    wins: int
    losses: int
    avg_confidence: Optional[float] = None
