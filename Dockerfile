FROM python:3.12-slim

# AWS Lambda Web Adapter: proxies Lambda invocations to the local HTTP server.
# No-op outside Lambda, so the same image runs locally and in Docker Compose.
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.0 /lambda-adapter /opt/extensions/lambda-adapter

RUN apt-get update && \
    apt-get install -y git curl gcc && \
    rm -rf /var/lib/apt/lists/* && \
    pip install uv --no-cache-dir

WORKDIR /app

COPY pyproject.toml uv.lock .

# Install the locked dependency set (ludic 0.5.x breaks against the latest
# starlette, so we must honor uv.lock rather than re-resolving).
RUN mkdir web && \
    touch web/__init__.py && \
    touch README.md && \
    uv export --frozen --no-dev --no-emit-project --format requirements-txt > /tmp/requirements.txt && \
    uv pip install --system --no-deps -r /tmp/requirements.txt && \
    uv pip install --system --no-deps .

COPY web web
COPY static static

USER nobody

EXPOSE 8000

CMD ["uvicorn", "web.server:app", "--host", "0.0.0.0", "--port", "8000"]
