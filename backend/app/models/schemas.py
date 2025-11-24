#!/usr/bin/env python3
"""Author: mansour.

Description:

"""

from pydantic import BaseModel, Field


class Word(BaseModel):
    """A word to be guessed."""

    id: int | None = None
    text: str = Field(min_length=1)


class Hint(BaseModel):
    """A hint given by an agent or human."""

    text: str = Field(min_length=1)


class Guess(BaseModel):
    """A guess made by an agent or human."""

    text: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class RoundResult(BaseModel):
    """Round result."""

    word: Word
    correct: bool
    hints_used: int
    score: float


class LeaderboardEntry(BaseModel):
    """Leaderboard entry."""

    participant: str
    wins: int
    losses: int
    avg_confidence: float | None = None
