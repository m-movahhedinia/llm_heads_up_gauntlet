#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from fastapi import APIRouter

from app.models.schemas import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/", response_model=list[LeaderboardEntry])
def get_leaderboard() -> list[LeaderboardEntry]:
    # Placeholder: static leaderboard
    return [
        LeaderboardEntry(participant="Agent A", wins=5, losses=2, avg_confidence=0.8),
        LeaderboardEntry(participant="Agent B", wins=3, losses=4, avg_confidence=0.6),
    ]
