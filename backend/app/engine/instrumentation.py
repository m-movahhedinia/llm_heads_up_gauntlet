#!/usr/bin/env python3
"""Author: mansour

Description:
Exampl:
from app.engine.instrumentation import instrument_guarded
chain = instrument_guarded("hint", build_hint_agent())
out = chain.invoke({})
"""

import time

from app.obs.metrics import errors_total, observe_step
from app.obs.tracing import instrument_lcel


def instrument_guarded(step_name: str, chain):
    chain = instrument_lcel(chain, f"step.{step_name}")
    from langchain_core.runnables import RunnableLambda

    def _invoke(input):
        start = time.perf_counter()
        try:
            out = chain.invoke(input)
            observe_step(step_name, (time.perf_counter() - start) * 1000)
            return out
        except Exception as e:
            errors_total.labels(step=step_name, type=e.__class__.__name__).inc()
            observe_step(step_name, (time.perf_counter() - start) * 1000)
            raise

    return RunnableLambda(_invoke)
