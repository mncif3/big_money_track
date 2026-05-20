FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    liblzma5 libxml2 gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir \
    fastapi>=0.110 uvicorn[standard]>=0.27 \
    sqlalchemy[asyncio]>=2.0 asyncpg>=0.29 alembic>=1.13 \
    apscheduler>=3.10 redis>=5.0 httpx>=0.26 \
    pandas>=2.2 numpy>=1.26 \
    akshare>=1.12 efinance>=0.5 \
    pydantic-settings>=2.2 python-multipart>=0.0.9 websockets>=12.0

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
