FROM python:3.11.4-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry and Python dependencies
RUN pip install --no-cache-dir poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --only=main

# Copy application
COPY app ./app

# Expose port (Render will use PORT env var)
EXPOSE $PORT

# Start command
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
