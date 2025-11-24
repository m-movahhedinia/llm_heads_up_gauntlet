#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from pydantic import BaseModel, Field

# TODO Make this more generic
class SafeGenParams(BaseModel):
    temperature: float = Field(ge=0.0, le=2.0, default=0.7)
    top_k: int = Field(ge=1, le=20, default=3)
    max_tokens: int = Field(ge=32, le=4096, default=256)
