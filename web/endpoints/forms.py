from ludic.catalog.headers import H1
from ludic.web import LudicApp, Request

from web.pages import Page

app = LudicApp()


@app.get("/forms/")
def forms(request: Request) -> Page:
    return Page(
        H1("Forms"),
        request=request,
        active_item="forms",
    )
