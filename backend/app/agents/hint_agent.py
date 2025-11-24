#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.tools import tool
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from app.agents.schemas import HintOutput
from app.knowledge.rag import build_faiss_rag_hint_chain
from app.knowledge.processors import build_hint_compressor
from app.agents.llm_provider import ProviderFactory

@tool
def rag_hint_tool(question: str) -> str:
    """Generate a concise hint via RAG for a target word."""
    chain = build_faiss_rag_hint_chain()
    return chain.invoke(question)

@tool
def compress_hint_tool(text: str) -> str:
    """Compress a hint using LLMLingua 2."""
    comp = build_hint_compressor()
    return comp.invoke(text)

def build_hint_agent(provider_name: str):
    llm = ProviderFactory.get_provider(provider_name)
    parser = PydanticOutputParser(pydantic_object=HintOutput)
    system = PromptTemplate(
        template=(
            "You are a hinting agent. Use tools when helpful to craft a concise, informative hint. "
            "Prefer RAG to enrich context, then compress if the hint is verbose. "
            "{format_instructions}"
        ),
        input_variables=[],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = system | llm.bind_tools([rag_hint_tool, compress_hint_tool]) | parser
    return chain
