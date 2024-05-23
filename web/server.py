from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypedDict

from ludic.catalog.headers import H1
from ludic.catalog.typography import Paragraph
from ludic.html import style
from ludic.styles.themes import (
    Cover,
    Fonts,
    Grid,
    Header,
    Headers,
    Layouts,
    LightTheme,
    Sidebar,
    set_default_theme,
)
from ludic.styles.types import Size
from ludic.web import LudicApp, Request
from ludic.web.routing import Mount
from starlette.middleware import Middleware
from starlette.staticfiles import StaticFiles

from .endpoints import (
    catalog,
    demos,
    docs,
    examples,
    index,
    search,
)
from .middlewares import CookieStorageMiddleware
from .pages import Page
from .search import Index, build_index

theme = LightTheme(
    measure=Size(70, "rem"),
    fonts=Fonts(size=Size(1.01, "em")),
    headers=Headers(
        h2=Header(size=Size(2.5, "em"), anchor=True),
        h3=Header(size=Size(2, "em"), anchor=True),
        h4=Header(size=Size(1.5, "em"), anchor=True),
    ),
    layouts=Layouts(
        grid=Grid(cell_size=Size(200, "px")),
        sidebar=Sidebar(side_width=Size(14, "rem")),
        cover=Cover(element="div.cover-main"),
    ),
)
set_default_theme(theme)


class State(TypedDict):
    index: Index


@asynccontextmanager
async def lifespan(app: LudicApp) -> AsyncIterator[State]:
    style.load(cache=True)
    yield {"index": build_index(app)}


app = LudicApp(
    debug=True,
    lifespan=lifespan,
    routes=index.app.routes
    + search.app.routes
    + [
        Mount("/demos", demos.router),
        Mount("/docs", docs.router, name="docs"),
        Mount("/catalog", catalog.router, name="catalog"),
        Mount("/examples", examples.router, name="examples"),
        Mount("/static", StaticFiles(directory="static"), name="static"),
    ],
    middleware=[Middleware(CookieStorageMiddleware)],
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
