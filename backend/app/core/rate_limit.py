#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, window_s=60, max_requests=60):
        self.window = window_s
        self.max = max_requests
        self.store = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.time()
        timestamps = [t for t in self.store[key] if now - t <= self.window]
        timestamps.append(now)
        self.store[key] = timestamps
        return len(timestamps) <= self.max
