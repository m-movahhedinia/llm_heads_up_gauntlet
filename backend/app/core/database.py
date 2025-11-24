#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings

ENGINE = create_async_engine(settings.database_url, echo=settings.debug)

ASYNC_SESSION = sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with ENGINE.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
