from ludic.catalog.headers import H1
from ludic.web import Request

from web.pages import Page


async def index(request: Request) -> Page:
    return Page(
        H1("Components and Styling"),
        request=request,
        active_item="examples:index",
    )
