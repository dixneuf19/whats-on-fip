FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --extra telegram

COPY ./whats_on_fip /whats_on_fip

CMD ["uv", "run", "python", "-m", "whats_on_fip.telegram.bot"]
