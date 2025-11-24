#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
import pytest
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.repositories.words import add_word, get_curated_words

@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with async_session() as s:
        yield s

@pytest.mark.asyncio
async def test_add_and_get_word(session):
    await add_word(session, "testword")
    words = await get_curated_words(session)
    assert len(words) == 1
    assert words[0].text == "testword"
