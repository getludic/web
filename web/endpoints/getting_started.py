from ludic.catalog.headers import H1
from ludic.web import LudicApp, Request

from web.pages import PageWithMenu

app = LudicApp()


@app.get("/getting-started/")
def getting_started(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Getting Started"),
        request=request,
        active_item="getting_started",
    )
