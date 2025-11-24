#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from fastapi import APIRouter

from app.engine.graphs import run_flip_script_round, run_heads_up_round
from app.engine.state import RoundState
from app.models.schemas import RoundResult, Word

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/start", response_model=Word)
def start_game() -> Word:
    # Placeholder: always start with "logic"
    return Word(id=100, text="logic")


@router.post("/rounds/{round_id}/submit", response_model=RoundResult)
def submit_round(round_id: int) -> RoundResult:
    # Placeholder: always return success
    return RoundResult(
        word=Word(id=round_id, text="logic"),
        correct=True,
        hints_used=1,
        score=1.0,
    )


@router.post("/play/heads-up", response_model=RoundState)
def play_heads_up(word: str, provider: str = "openai", compress_hints: bool = True) -> RoundState:
    return run_heads_up_round(word=word, provider_name=provider, compress_hints=compress_hints)


@router.post("/play/flip-script", response_model=RoundState)
def play_flip_script(word: str, provider: str = "openai") -> RoundState:
    return run_flip_script_round(word=word, provider_name=provider)
