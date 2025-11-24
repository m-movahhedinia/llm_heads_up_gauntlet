#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from app.knowledge.embeddings import get_embedding_provider

def test_embedding_provider():
    provider = get_embedding_provider()
    vecs = provider.embed_documents(["hello world", "test"])
    assert len(vecs) == 2
    assert len(vecs[0]) > 0
