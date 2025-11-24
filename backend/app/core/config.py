#!/usr/bin/env python3
"""Author: mansour.

Description:

"""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class ProviderSettings(BaseModel):
    hf_model: str = Field(default=os.getenv("HF_MODEL", "microsoft/Phi-4-mini-instruct"))
    hf_api_token: str | None = Field(default=os.getenv("HF_API_TOKEN"))

    openai_model: str = Field(default=os.getenv("OPENAI_MODEL", "gpt-5-nano-2025-08-07"))
    openai_api_key: str | None = Field(default=os.getenv("OPENAI_API_KEY"))

    anthropic_model: str = Field(default=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"))
    anthropic_api_key: str | None = Field(default=os.getenv("ANTHROPIC_API_KEY"))

    default_timeout_seconds: int = Field(default=int(os.getenv("LLM_TIMEOUT", "30")))
    default_max_retries: int = Field(default=int(os.getenv("LLM_RETRIES", "2")))
    temperature: float = Field(default=float(os.getenv("LLM_TEMPERATURE", "0.7")))
    top_p: float = Field(default=float(os.getenv("LLM_TOP_P", "0.9")))
    max_tokens: int = Field(default=int(os.getenv("LLM_MAX_TOKENS", "512")))


class Settings(BaseModel):
    """Application settings."""

    app_name: str = Field(default="Multi-Agent Game Backend")
    environment: str = Field(default=os.getenv("ENVIRONMENT", "development"))
    debug: bool = Field(default=os.getenv("DEBUG", "true").lower() == "true")
    log_level: str = Field(default=os.getenv("LOG_LEVEL", "INFO"))
    api_prefix: str = Field(default=os.getenv("API_PREFIX", "/api/v1"))
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///database.db"))
    pinecone_api_key: str | None = Field(default=os.getenv("PINECONE_API_KEY"))
    compress_prompts: bool = Field(default=os.getenv("COMPRESS_PROMPTS", "false").lower() == "false")
    model_provider_settings: ProviderSettings = Field(default=ProviderSettings())


settings = Settings()
