# Ludic Web

This is the homepage for [The Ludic Framework](https://github.com/getludic/ludic) written with Ludic.

## Running

With docker:

```
docker compose -f docker-compose.dev.yaml build
docker compose -f docker-compose.dev.yaml up
```

With UV:

```
uv sync
uv run uvicorn --reload web.server:app
```

In both cases, the app is running at `http://localhost:8000`.
