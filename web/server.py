from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from ludic.catalog.headers import H1
from ludic.catalog.typography import Paragraph
from ludic.html import style
from ludic.styles.themes import Fonts, Header, Headers, LightTheme, set_default_theme
from ludic.styles.types import Size
from ludic.web import LudicApp
from ludic.web.routing import Mount
from starlette.staticfiles import StaticFiles

from .endpoints import (
    catalog,
    components,
    examples,
    forms,
    getting_started,
    htmx,
    index,
    layouts,
    styles,
    tables,
    web_framework,
)
from .pages import Page

theme = LightTheme(
    fonts=Fonts(size=Size(1.01, "em")),
    headers=Headers(
        h2=Header(size=Size(2.5, "em"), anchor=True),
        h3=Header(size=Size(2, "em"), anchor=True),
        h4=Header(size=Size(1.5, "em"), anchor=True),
    ),
)
set_default_theme(theme)


@asynccontextmanager
async def lifespan(_: LudicApp) -> AsyncIterator[None]:
    style.load(cache=True)
    yield


app = LudicApp(
    debug=True,
    lifespan=lifespan,
    routes=(
        examples.app.routes
        + index.app.routes
        + catalog.app.routes
        + components.app.routes
        + forms.app.routes
        + tables.app.routes
        + web_framework.app.routes
        + htmx.app.routes
        + styles.app.routes
        + layouts.app.routes
        + getting_started.app.routes
        + [
            Mount("/static", StaticFiles(directory="static"), name="static"),
        ]
    ),
)


@app.exception_handler(404)
async def not_found() -> Page:
    return Page(
        H1("Page Not Found"),
        Paragraph("The page you are looking for was not found."),
    )


@app.exception_handler(500)
async def server_error() -> Page:
    return Page(
        H1("Server Error"),
        Paragraph("Server encountered an error during processing."),
    )
