FROM python:3.11-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS app

COPY alembic.ini .
COPY ./src ./src
