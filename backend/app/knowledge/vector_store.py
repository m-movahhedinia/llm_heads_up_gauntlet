#!/usr/bin/env python3
"""Author: mansour

Description:

"""

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from app.core.config import settings


class VectorStoreFactory:
    @staticmethod
    def create_faiss(embeddings) -> FAISS:
        sample_vector = embeddings.embed_query("test")
        dim = len(sample_vector)
        faiss_index = faiss.IndexFlatL2(dim)
        return FAISS(
            embedding_function=embeddings, index=faiss_index, docstore=InMemoryDocstore(), index_to_docstore_id={}
        )

    @staticmethod
    def create_pinecone(index_name: str, embedding: Embeddings) -> PineconeVectorStore:
        pinecone = Pinecone(api_key=settings.pinecone_api_key)
        if not pinecone.has_index(index_name):
            pinecone.create_index(
                index_name, dimension=1536, metric="cosine", spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        return PineconeVectorStore(pinecone.Index(index_name), embedding=embedding)
