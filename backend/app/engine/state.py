#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from enum import Enum

from pydantic import BaseModel

from app.agents.schemas import GuessOutput, HintOutput, JudgeOutput


class GameMode(Enum):
    HEADS_UP = "heads_up"
    FLIP_SCRIPT = "flip_script"


class RoundConfig(BaseModel):
    mode: GameMode
    word: str
    provider_name: str = "openai"
    compress_hints: bool = True
    top_k: int = 3
    temperature: float = 0.7
    max_tokens: int = 256


class RoundState(BaseModel):
    config: RoundConfig
    hints: list[HintOutput] = []
    compressed_hints: list[str] = []
    guesses: list[GuessOutput] = []
    judgment: JudgeOutput | None = None
    logs: list[str] = []
