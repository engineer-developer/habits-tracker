FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./fastapi-app/pyproject.toml .

RUN uv venv
RUN uv sync

ENV PATH="/usr/app/.venv/bin:$PATH"

COPY docker/fastapi_app/entrypoint.sh /usr/scripts/
RUN chmod +x /usr/scripts/entrypoint.sh

COPY ./fastapi-app/src/ ./src/

WORKDIR /usr/app/src/

ENTRYPOINT ["/usr/scripts/entrypoint.sh"]