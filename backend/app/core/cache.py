#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from functools import lru_cache

@lru_cache(maxsize=1024)
def memo(key: str, value: str) -> str:
    return value

def with_cache(runnable, key_fn=lambda x: str(x)):
    from langchain_core.runnables import RunnableLambda
    def _invoke(input):
        k = key_fn(input)
        try:
            return memo(k, memo.cache_parameters)  # noop trick — we need to compute
        except Exception:
            out = runnable.invoke(input)
            memo(k, out if isinstance(out, str) else getattr(out, "content", str(out)))
            return out
    return RunnableLambda(_invoke)
