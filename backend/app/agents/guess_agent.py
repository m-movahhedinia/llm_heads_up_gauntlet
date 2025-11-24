#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from app.agents.schemas import GuessOutput
from app.agents.llm_provider import ProviderFactory

def build_guess_agent(provider_name: str):
    llm = ProviderFactory.get_provider(provider_name)
    parser = PydanticOutputParser(pydantic_object=GuessOutput)
    system = PromptTemplate(
        template=(
            "You are a guessing agent. Read the hints and return a single-word guess and confidence.\n"
            "{format_instructions}"
        ),
        input_variables=[],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    prompt = PromptTemplate(
        template="Hints: {hints}",
        input_variables=["hints"],
    )
    chain = system | prompt | llm | parser
    return chain
