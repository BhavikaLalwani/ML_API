FROM python:3.11.4-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry
COPY pyproject.toml README.md ./
RUN poetry config virtualenvs.create false
RUN poetry install --only=main

COPY app ./app

EXPOSE $PORT

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
