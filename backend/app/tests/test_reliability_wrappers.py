#!/usr/bin/env python3
"""Author: mansour

Description:

"""

import asyncio

import pytest
from langchain_core.runnables import RunnableLambda

from app.core.reliability import CircuitBreaker, with_circuit_breaker, with_retry, with_timeout


def test_timeout():
    async def slow(_):
        await asyncio.sleep(0.2)
        return "ok"

    chain = with_timeout(RunnableLambda(lambda x: asyncio.run(slow(x))), seconds=0.05)
    with pytest.raises(Exception):
        chain.invoke({})


def test_retry_success():
    calls = {"n": 0}

    async def flaky(_):
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError("flaky")
        return "ok"

    chain = with_retry(RunnableLambda(lambda x: asyncio.run(flaky(x))), attempts=2)
    assert chain.invoke({}) == "ok"


def test_circuit():
    br = CircuitBreaker(fail_threshold=1, cool_down=0.1)

    async def bad(_):
        raise RuntimeError("fail")

    chain = with_circuit_breaker(RunnableLambda(lambda x: asyncio.run(bad(x))), br)
    with pytest.raises(Exception):
        chain.invoke({})
    with pytest.raises(Exception):
        chain.invoke({})
