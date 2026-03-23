FROM ghcr.io/astral-sh/uv:0.6 AS uv
FROM python:3.14-slim
COPY --from=uv /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-install-project --dev
COPY . .
EXPOSE 8000
