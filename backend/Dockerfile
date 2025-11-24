FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifests first for caching
COPY backend/pyproject.toml backend/uv.lock* /app/
RUN pip install --no-cache-dir uv && uv sync --frozen

# Copy source code
COPY backend /app/backend

# Environment defaults
ENV LOG_LEVEL=INFO \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318 \
    PROMETHEUS_MULTIPROC_DIR=/tmp

EXPOSE 8000

CMD ["python", "-m", "backend.app"]
