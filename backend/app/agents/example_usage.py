#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from app.agents.llm_provider import ProviderFactory, generate_structured
from app.agents.schemas import HintOutput


async def demo():
    provider = ProviderFactory.get_provider("huggingface")
    return generate_structured(provider, "Give me a hint for the word 'entropy'.", HintOutput)
