#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from typing import Any, AsyncGenerator

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import ASYNC_SESSION
from app.models.schemas import Word
from app.repositories.words import get_curated_words, add_word

router = APIRouter(prefix="/words", tags=["words"])

async def get_session() -> AsyncGenerator[Any, Any]:
    async with ASYNC_SESSION() as session:
        yield session

@router.get("/curated", response_model=list[Word])
async def curated(session: AsyncSession = Depends(get_session)):
    words = await get_curated_words(session)
    return [Word(id=w.id, text=w.text) for w in words]

@router.post("/", response_model=Word)
async def create_word(word: Word, session: AsyncSession = Depends(get_session)):
    new_word = await add_word(session, word.text)
    return Word(id=new_word.id, text=new_word.text)

@router.get("/random", response_model=Word)
def get_random_word() -> Word:
    # Placeholder: return one static word
    return Word(id=99, text="neural")
