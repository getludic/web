from ludic.catalog.headers import H1
from ludic.web import Request

from web.pages import Page


def forms(request: Request) -> Page:
    return Page(
        H1("Forms"),
        request=request,
        active_item="forms",
    )
