#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from dataclasses import dataclass


@dataclass
class TokenBudget:
    max_round_tokens: int = 4000
    used: int = 0

    def charge(self, n: int):
        self.used += n
        if self.used > self.max_round_tokens:
            raise RuntimeError("token_budget_exceeded")
