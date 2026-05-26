import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypedDict

from ludic.catalog.headers import H1
from ludic.catalog.typography import Paragraph
from ludic.html import style
from ludic.styles import themes
from ludic.web import LudicApp, Request
from ludic.web.routing import Mount
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.staticfiles import StaticFiles

from . import config
from .endpoints import (
    catalog,
    demos,
    docs,
    essential,
    examples,
    index,
    search,
    status,
)
from .middlewares import (
    CookieStorageMiddleware,
    PerformanceMiddleware,
    ProfileMiddleware,
    SecurityHeadersMiddleware,
    TrustForwardedHostMiddleware,
)
from .pages import Page
from .search import Index, build_index
from .search.cache import load_from_s3
from .themes import theme

themes.set_default_theme(theme)


class State(TypedDict):
    index: Index
    theme: themes.Theme


@asynccontextmanager
async def lifespan(app: LudicApp) -> AsyncIterator[State]:
    style.load(cache=True)

    index: Index | None = None
    if bucket := os.environ.get("INDEX_S3_BUCKET"):
        index = load_from_s3(bucket)
    if index is None:
        index = await build_index(app)

    yield {
        "index": index,
        "theme": themes.get_default_theme(),
    }


middlewares = [
    # Must come first: rewrites Host/scheme from X-Forwarded-* so every
    # downstream middleware and the app see the public URL, not the Lambda URL.
    Middleware(TrustForwardedHostMiddleware),
    Middleware(SecurityHeadersMiddleware),
    Middleware(GZipMiddleware, minimum_size=1000),
    Middleware(PerformanceMiddleware),
    Middleware(CookieStorageMiddleware),
]
if config.ENABLE_PROFILING:
    middlewares.append(Middleware(ProfileMiddleware))


app = LudicApp(
    debug=config.DEBUG,
    lifespan=lifespan,
    routes=index.app.routes
    + search.app.routes
    + essential.app.routes
    + [
        Mount("/demos", demos.router),
        Mount("/docs", docs.router, name="docs"),
        Mount("/catalog", catalog.router, name="catalog"),
        Mount("/examples", examples.router, name="examples"),
        Mount("/status", status.app, name="status"),
        Mount("/static", StaticFiles(directory="static"), name="static"),
    ],
    middleware=middlewares,
)


@app.exception_handler(404)
async def not_found(request: Request) -> Page:
    return Page(
        H1("Page Not Found"),
        Paragraph("The page you are looking for was not found."),
        request=request,
        active_item=None,
    )


@app.exception_handler(500)
async def server_error(request: Request) -> Page:
    return Page(
        H1("Server Error"),
        Paragraph("Server encountered an error during processing."),
        request=request,
        active_item=None,
    )
