FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --extra telegram

COPY ./whats_on_fip ./whats_on_fip

CMD ["python", "-m", "whats_on_fip.telegram.bot"]
