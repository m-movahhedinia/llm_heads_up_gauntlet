#!/usr/bin/env python3
"""Author: mansour

Description:

"""

import pytest

from app.memory.episodic_store import init_memory_db, read_items, write_item
from app.memory.schemas import MemoryItem


@pytest.mark.asyncio
async def test_episodic_write_read():
    await init_memory_db()
    await write_item(MemoryItem(kind="hint", content="disorder increases", word="entropy"))
    items = await read_items("entropy")
    assert items and items[0].content == "disorder increases"
