from ludic.catalog.headers import H1
from ludic.web import LudicApp, Request

from web.pages import PageWithMenu

app = LudicApp()


@app.get("/forms/")
def forms(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Forms"),
        request=request,
        active_item="forms",
    )
