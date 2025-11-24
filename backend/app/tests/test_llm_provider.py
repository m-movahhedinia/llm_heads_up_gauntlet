#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from langchain_core.runnables import Runnable

from app.agents.llm_provider import ProviderFactory, generate_structured
from app.agents.schemas import HintOutput


class DummyProvider(Runnable):
    def invoke(self, inputs, config=None):
        return '{"hint": "test-hint", "rationale": "test-rationale"}'


def test_generate_structured():
    provider = DummyProvider()
    result = generate_structured(provider, "hint please", HintOutput)
    assert result.hint == "test-hint"
    assert result.rationale == "test-rationale"


def test_provider_factory_openai():
    prov = ProviderFactory.get_provider("openai")
    assert prov is not None
