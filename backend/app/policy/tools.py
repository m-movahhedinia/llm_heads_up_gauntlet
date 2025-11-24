#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from langchain_core.tools import tool

from app.policy.learner import propose_policy_update
from app.policy.schemas import PolicyUpdateInput, PolicyUpdateOutput


@tool
def update_policy_tool(input_: PolicyUpdateInput) -> PolicyUpdateOutput:
    """Propose a small, safe update to the current policy based on round metrics and memory signals."""
    return propose_policy_update(input_)
