#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
import os
from pydantic import BaseModel, Field

# TODO Deprecated, move to config
class Secrets(BaseModel):
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY") or "")
    anthropic_api_key: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY") or "")
    hf_api_token: str = Field(default_factory=lambda: os.getenv("HF_API_TOKEN") or "")

    def validate_required(self):
        missing = [k for k, v in self.model_dump().items() if not v]
        if missing:
            raise RuntimeError(f"Missing secrets: {missing}")

secrets = Secrets()
