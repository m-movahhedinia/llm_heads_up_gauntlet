#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts.prompt import PromptTemplate

from app.agents.llm_provider import ProviderFactory
from app.agents.schemas import JudgeOutput


def build_judge_agent(provider_name: str):
    llm = ProviderFactory.get_provider(provider_name)
    parser = PydanticOutputParser(pydantic_object=JudgeOutput)
    prompt = PromptTemplate(
        template=(
            "Target word: {word}\nGuess: {guess}\n"
            "Judge correctness and return normalized score with brief feedback.\n"
            "{format_instructions}"
        ),
        input_variables=["word", "guess"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm | parser
    return chain
