#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from hashlib import sha256

from langchain_core.documents import Document

from app.knowledge.embeddings import get_embedding_provider
from app.knowledge.vector_store import VectorStoreFactory


def test_faiss_store():
    embeddings = get_embedding_provider()
    docs = [
        Document(page_content="quantum mechanics", metadata={"role": "subject"}),
        Document(page_content="entropy", metadata={"role": "subject"}),
        Document(page_content="neural networks", metadata={"role": "subject"}),
    ]
    ids = [sha256(doc.page_content.lower().strip().encode()).hexdigest() for doc in docs]
    store = VectorStoreFactory.create_faiss(embeddings)
    stored_docs = store.add_documents(documents=docs, ids=ids)
    results = store.similarity_search("quantum mechanics", k=2, filter={"role": "subject"})
    assert len(stored_docs) == len(docs)
    assert len(results) > 0
    assert isinstance(results[0].page_content, str)
