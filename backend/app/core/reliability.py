#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
import asyncio, random
from langchain_core.runnables import RunnableLambda

def with_timeout(runnable, seconds: float = 30.0):
    async def _invoke(input_):
        return await asyncio.wait_for(runnable.ainvoke(input_), timeout=seconds)
    return RunnableLambda(lambda x: asyncio.run(_invoke(x)))

def with_retry(runnable, attempts: int = 2, base_delay: float = 0.5):
    async def _invoke(input_):
        last = None
        for i in range(attempts + 1):
            try:
                return await runnable.ainvoke(input_)
            except Exception as e:
                last = e
                await asyncio.sleep(base_delay * (2 ** i))
        raise last
    return RunnableLambda(lambda x: asyncio.run(_invoke(x)))

class CircuitBreaker:
    def __init__(self, fail_threshold=3, cool_down=10.0):
        self.failures = 0
        self.open_until = 0.0
        self.fail_threshold = fail_threshold
        self.cool_down = cool_down
    async def wrap(self, runnable, input_):
        import time
        now = time.time()
        if now < self.open_until:
            raise RuntimeError("circuit_open")
        try:
            out = await runnable.ainvoke(input_)
            self.failures = 0
            return out
        except Exception:
            self.failures += 1
            if self.failures >= self.fail_threshold:
                self.open_until = now + self.cool_down
            raise

def with_circuit_breaker(runnable, breaker: CircuitBreaker):
    async def _invoke(input_):
        return await breaker.wrap(runnable, input_)
    return RunnableLambda(lambda x: asyncio.run(_invoke(x)))