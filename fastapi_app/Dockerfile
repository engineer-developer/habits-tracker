FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt update && apt install -y python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN pip install pipx

ENV PATH="/root/.local/bin:${PATH}"

RUN pipx install poetry && poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --only main

ENV PYTHONPATH=./src/fastapi_app/

COPY src/ ./src/