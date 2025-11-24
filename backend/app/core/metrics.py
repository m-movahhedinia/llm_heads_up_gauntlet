#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from dataclasses import dataclass

# TODO Move other metrics here. Including performance metrics.
@dataclass
class ReliabilityMetrics:
    timeouts: int = 0
    retries: int = 0
    circuit_opens: int = 0
