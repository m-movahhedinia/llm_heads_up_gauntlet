#!/usr/bin/env python3
"""
Author: mansour

Description:

"""

from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_provider(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Returns a HuggingFace embedding provider using LangChain wrapper.
    """
    return HuggingFaceEmbeddings(model_name=model_name)
