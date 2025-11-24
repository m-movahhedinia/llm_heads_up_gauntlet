#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from prometheus_client import Counter, Histogram

rounds_total = Counter("rounds_total", "Total rounds played", ["mode"])
agent_step_total = Counter("agent_step_total", "Agent steps executed", ["step"])
latency_ms = Histogram("latency_ms", "Step latency in ms", ["step"])
errors_total = Counter("errors_total", "Total errors", ["step", "type"])
tokens_used = Counter("tokens_used", "Tokens used per round", ["step"])


def observe_step(step: str, ms: float, tokens: int | None = None):
    latency_ms.labels(step=step).observe(ms / 1000.0)
    agent_step_total.labels(step=step).inc()
    if tokens is not None:
        tokens_used.labels(step=step).inc(tokens)
