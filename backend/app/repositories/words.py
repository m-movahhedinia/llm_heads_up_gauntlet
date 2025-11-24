#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.db_models import WordDB
from typing import  Sequence

async def get_curated_words(session: AsyncSession) -> Sequence[WordDB]:
    result = await session.exec(select(WordDB))
    return result.all()

async def add_word(session: AsyncSession, text: str) -> WordDB:
    word = WordDB(text=text)
    session.add(word)
    await session.commit()
    await session.refresh(word)
    return word
