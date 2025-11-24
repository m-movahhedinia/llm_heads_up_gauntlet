#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from hashlib import sha256

from langchain_core.documents import Document
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from app.agents.llm_provider import ProviderFactory
from app.knowledge.embeddings import get_embedding_provider
from app.knowledge.vector_store import VectorStoreFactory


# TODO Unify these functions into a configurable single one.
def build_faiss_rag_hint_chain(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    embeddings = get_embedding_provider(model_name=model_name)
    # TODO Make configurable
    store = VectorStoreFactory.create_faiss(embeddings)
    retriever = store.as_retriever(search_kwargs={"k": 3})
    # TODO Make configurable
    llm = ProviderFactory.get_provider("huggingface")
    # TODO Move to configs and make it a propper jinja template. Host it somewhere.
    hint_prompt = PromptTemplate(
        template=(
            "You are generating a concise hint for the target concept.\n"
            "Context:\n{context}\n\n"
            "Target: {question}\n"
            "Return a single short hint that is informative but does not reveal the exact word."
        ),
        input_variables=["context", "question"],
    )

    # Compose: retriever provides context, passthrough carries question, prompt -> llm
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | hint_prompt
        | llm
        | RunnableLambda(lambda x: getattr(x, "content", str(x)))  # TODO Replace with an output parser
    )
    return chain


def build_pinecone_rag_hint_chain(
    index_name: str, texts: list[str], model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
):
    embeddings = get_embedding_provider(model_name=model_name)
    store = VectorStoreFactory.create_pinecone(index_name, embeddings)
    retriever = store.as_retriever(search_kwargs={"k": 3})
    llm = ProviderFactory.get_provider("huggingface")

    hint_prompt = PromptTemplate(
        template=(
            "You are generating a concise hint for the target concept.\n"
            "Context:\n{context}\n\n"
            "Target: {question}\n"
            "Return a single short hint that is informative but does not reveal the exact word."
        ),
        input_variables=["context", "question"],
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | hint_prompt
        | llm
        | RunnableLambda(lambda x: getattr(x, "content", str(x)))
    )
    return chain


def build_docs_rag_hint_chain(docs: list[Document], model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    # Sometimes you already have Document objects; build FAISS from them.
    embeddings = get_embedding_provider(model_name=model_name)
    # TODO Make configurable
    store = VectorStoreFactory.create_faiss(embeddings)
    retriever = store.as_retriever(search_kwargs={"k": 3})
    # TODO Make configurable
    llm = ProviderFactory.get_provider("huggingface")
    hint_prompt = PromptTemplate(
        template=(
            "You are generating a concise hint for the target concept.\n"
            "Context:\n{context}\n\n"
            "Target: {question}\n"
            "Return a single short hint that is informative but does not reveal the exact word."
        ),
        input_variables=["context", "question"],
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | hint_prompt
        | llm
        | RunnableLambda(lambda x: getattr(x, "content", str(x)))
    )
    return chain


# TODO Remove this
def demo_rag_debug() -> list[Document]:
    # Create vector store or vector db
    embeddings = get_embedding_provider()
    vector_store = VectorStoreFactory.create_faiss(embeddings)

    # Add documents
    docs = [
        Document(page_content="quantum mechanics", metadata={"role": "subject"}),
        Document(page_content="entropy", metadata={"role": "subject"}),
        Document(page_content="neural networks", metadata={"role": "subject"}),
    ]

    ids = [sha256(doc.page_content.lower().strip().encode()).hexdigest() for doc in docs]

    _ = vector_store.add_documents(documents=docs, ids=ids)

    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # Retrieve documents
    results = retriever.similarity_search("physics", k=2, filter={"role": "subject"})
    return results
