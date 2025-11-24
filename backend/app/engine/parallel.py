#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from langchain_core.runnables import RunnableParallel, RunnableLambda

def parallel_map(runnable, items):
    chain = RunnableParallel(**{f"i{i}": RunnableLambda(lambda x, it=it: runnable.invoke(it))
                                for i, it in enumerate(items)})
    out = chain.invoke({})
    return [out[k] for k in sorted(out.keys())]
