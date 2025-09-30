FROM python:3.11.4-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential gcc g++ python3-dev && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
