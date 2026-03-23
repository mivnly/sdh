FROM ghcr.io/astral-sh/uv:0.6 AS uv
FROM python:3.14-slim
COPY --from=uv /uv /uvx /bin/
WORKDIR /app
ENV UV_LINK_MODE=copy
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-install-project --no-dev
COPY . .
EXPOSE 8000
