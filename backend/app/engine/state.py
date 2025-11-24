#!/usr/bin/env python3
"""
Author: mansour

Description:

"""

from pydantic import BaseModel, Field
from typing import List, Optional
from app.agents.schemas import HintOutput, GuessOutput, JudgeOutput

from enum import Enum


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
    hints: List[HintOutput] = []
    compressed_hints: List[str] = []
    guesses: List[GuessOutput] = []
    judgment: Optional[JudgeOutput] = None
    logs: List[str] = []
