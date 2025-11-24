#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from pydantic import BaseModel, Field


class Policy(BaseModel):
    # LLM generation knobs
    temperature: float = Field(ge=0.0, le=2.0, default=0.7)
    max_tokens: int = Field(ge=32, le=4096, default=256)
    # Retrieval knobs
    retriever_k: int = Field(ge=1, le=20, default=3)
    # Compression knobs
    compression_rate: float = Field(ge=0.1, le=0.9, default=0.5)
    # Calibration knobs
    confidence_bias: float = Field(ge=-0.5, le=0.5, default=0.0)


class PolicyUpdateInput(BaseModel):
    policy: Policy
    accuracy: float = Field(ge=0.0, le=1.0)
    calibration: float = Field(ge=0.0, le=1.0)
    creativity: float = Field(ge=0.0, le=1.0)
    efficiency: float = Field(ge=0.0, le=1.0)
    summary_signals: str | None = None  # optional memory summary text


class PolicyUpdateOutput(BaseModel):
    new_policy: Policy
    rationale: str
