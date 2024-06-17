# Ludic Web

This is the homepage for [The Ludic Framework](https://github.com/getludic/ludic) written with Ludic.

## Running

With docker:

```
docker compose build
docker compose up
```

With Poetry:

```
poetry install
poetry run uvicorn --reload web.server:app
```

In both cases, the app is running at `http://localhost:8000`.
