FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y git curl gcc && \
    rm -rf /var/lib/apt/lists/* && \
    pip install poetry==1.8.3 --no-cache-dir

USER nobody

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock .

RUN mkdir web && \
    touch web/__init__.py && \
    touch README.md && \
    poetry install && \
    rm -rf $POETRY_CACHE_DIR

COPY web web
COPY static static

EXPOSE 8000

ENTRYPOINT ["poetry", "run"]

CMD ["uvicorn", "web.server:app", "--host", "0.0.0.0", "--port", "8000"]
