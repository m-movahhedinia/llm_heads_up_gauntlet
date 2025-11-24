#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from sqlmodel import SQLModel, Field, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from app.memory.schemas import MemoryItem

class MemoryDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kind: str
    content: str
    word: str
    confidence: float | None = None
    correct: bool | None = None
    score: float | None = None
    timestamp: str

# Setup (reuse app.core.database engine if available)
engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
# TODO Make this reusable
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_memory_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def write_item(item: MemoryItem) -> None:
    async with async_session() as s:
        m = MemoryDB(
            kind=item.kind, content=item.content, word=item.word,
            confidence=item.confidence, correct=item.correct, score=item.score,
            timestamp=item.timestamp.isoformat()
        )
        s.add(m)
        await s.commit()

async def read_items(word: str, kinds: List[str] | None = None) -> List[MemoryItem]:
    async with async_session() as s:
        query = select(MemoryDB).where(MemoryDB.word == word)
        if kinds:
            query = query.where(MemoryDB.kind.in_(kinds))
        rows = (await s.exec(query)).all()
        return [MemoryItem(
            kind=r.kind, content=r.content, word=r.word,
            confidence=r.confidence, correct=r.correct, score=r.score
        ) for r in rows]
