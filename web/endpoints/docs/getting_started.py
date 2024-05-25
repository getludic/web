from ludic.catalog.headers import H1
from ludic.web import Request

from web.pages import Page


def getting_started(request: Request) -> Page:
    return Page(
        H1("Getting Started"),
        request=request,
        active_item="getting_started",
        title="Ludic - Getting Started",
    )
