#!/usr/bin/env python3
"""
Author: mansour

Description:

"""

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts.prompt import PromptTemplate
from app.core.config import settings
from app.agents.schemas import HintOutput, GuessOutput, JudgeOutput

class ProviderFactory:
    @staticmethod
    def get_provider(name: str):
        name = name.lower()

        match name:
            case "openai" | "oai":
                return ChatOpenAI(
                    model=settings.model_provider_settings.openai_model,
                    api_key=settings.model_provider_settings.openai_api_key
                )
            case "anthropic" | "claude":
                return ChatAnthropic(
                    model=settings.model_provider_settings.anthropic_model,
                    api_key=settings.model_provider_settings.anthropic_api_key
                )
            case "hf" | "huggingface":
                return HuggingFaceEndpoint(
                    repo_id=settings.model_provider_settings.hf_model,
                    huggingfacehub_api_token=settings.model_provider_settings.hf_api_token
                )
            case _:
                raise ValueError(f"Unknown model provider: {name}")

def generate_structured(provider, prompt: str, schema):
    """
    Use LangChain's PydanticOutputParser to enforce structured outputs.
    """
    parser = PydanticOutputParser(pydantic_object=schema)
    template = PromptTemplate(
        template="{prompt}\n\n{format_instructions}",
        input_variables=["prompt"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = template | provider | parser
    return chain.invoke({"prompt": prompt})