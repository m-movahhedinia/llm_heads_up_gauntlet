#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from app.memory.schemas import MemoryItem

SummaryPrompt = PromptTemplate(
    template=(
        "You maintain semantic memory of prior rounds.\n"
        "Context:\n{context}\n\n"
        "Task: Extract 3-5 key signals, best hint patterns, and common mistakes "
        "that would improve future hinting and guessing for '{word}'.\n"
        "Return concise bullet points."
    ),
    input_variables=["context", "word"],
)


def build_faiss_memory_chain(items: list[MemoryItem]):
    texts = [f"{i.kind.upper()}: {i.content}" for i in items]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    store = FAISS.from_texts(texts, embeddings)
    retriever = store.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = (
        {"context": retriever, "word": RunnablePassthrough()}
        | SummaryPrompt
        | llm
        | RunnableLambda(lambda x: getattr(x, "content", str(x)))
    )
    return chain


def build_pinecone_memory_chain(index_name: str, items: list[MemoryItem]):
    texts = [f"{i.kind.upper()}: {i.content}" for i in items]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    store = PineconeVectorStore.from_texts(texts, embeddings, index_name=index_name)
    retriever = store.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = (
        {"context": retriever, "word": RunnablePassthrough()}
        | SummaryPrompt
        | llm
        | RunnableLambda(lambda x: getattr(x, "content", str(x)))
    )
    return chain
