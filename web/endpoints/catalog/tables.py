from ludic.catalog.headers import H1
from ludic.web import Request

from web.pages import Page


def tables(request: Request) -> Page:
    return Page(
        H1("Tables"),
        request=request,
        active_item="tables",
    )
