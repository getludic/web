import asyncio

from ludic.catalog.headers import H3
from ludic.catalog.layouts import Box
from ludic.catalog.loaders import LazyLoader
from ludic.web import LudicApp, Request

app = LudicApp()


@app.get("/")
async def index(request: Request) -> LazyLoader:
    return LazyLoader(load_url=request.url_for(load_content, seconds=3))


@app.get("/load/{seconds:int}")
async def load_content(seconds: int) -> Box:
    await asyncio.sleep(seconds)
    return Box(
        H3("Content loaded!", classes=["text-align-center"]),
        classes=["invert"],
        style={"padding-top": "10rem", "padding-bottom": "10rem"},
    )
