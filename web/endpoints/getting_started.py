from ludic.catalog.headers import H1
from ludic.web import LudicApp, Request

from web.pages import Page

app = LudicApp()


@app.get("/getting-started/")
def getting_started(request: Request) -> Page:
    return Page(
        H1("Getting Started"),
        request=request,
        active_item="getting_started",
    )
