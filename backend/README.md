# Backend (Phase 0)

- FastAPI app with health and root endpoints
- Env-driven configuration (Pydantic v2 + dotenv)
- Structured logging (Loguru)
- Core schemas for words, hints, guesses, round results
- Tests for health, config, logging

## Run
uv run uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000

## Test
uv run pytest