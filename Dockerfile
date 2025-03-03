FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y git curl gcc && \
    rm -rf /var/lib/apt/lists/* && \
    pip install uv --no-cache-dir

WORKDIR /app

COPY pyproject.toml uv.lock .

RUN mkdir web && \
    touch web/__init__.py && \
    touch README.md && \
    uv pip install --system .

COPY web web
COPY static static

USER nobody

EXPOSE 8000

CMD ["uvicorn", "web.server:app", "--host", "0.0.0.0", "--port", "8000"]
