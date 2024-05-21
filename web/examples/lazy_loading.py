import asyncio

from ludic.catalog.headers import H3
from ludic.catalog.layouts import Box, Frame
from ludic.catalog.loaders import LazyLoader
from ludic.web import LudicApp, Request

app = LudicApp()


@app.get("/")
async def index(request: Request) -> LazyLoader:
    return LazyLoader(load_url=request.url_for(load_content, seconds=2))


@app.get("/load/{seconds:int}")
async def load_content(seconds: int) -> Box:
    await asyncio.sleep(seconds)
    return Box(
        Frame(
            H3("Content Loaded", anchor=False),
        )
    )
