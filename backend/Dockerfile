FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    "fastapi>=0.116.0,<1.0.0" \
    "uvicorn[standard]>=0.32.0,<1.0.0" \
    "pydantic>=2.10.0,<3.0.0" \
    "neo4j>=5.28.0,<6.0.0" \
    "huggingface_hub>=0.30.0,<1.0.0" \
    "httpx>=0.28.0,<1.0.0" \
    "numpy>=2.1.0,<3.0.0"

COPY src /app/src

ENV PYTHONPATH=/app/src
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
