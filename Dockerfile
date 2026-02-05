FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_PYTHON=python3.11

COPY pyproject.toml uv.lock .
RUN uv sync --no-dev --frozen

RUN playwright install chromium

COPY app/ app/

EXPOSE 8000

CMD ["sh", "-c", "uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
