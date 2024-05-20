from ludic.catalog.headers import H1
from ludic.web import LudicApp, Request

from web.pages import Page

app = LudicApp()


@app.get("/tables/")
def tables(request: Request) -> Page:
    return Page(
        H1("Tables"),
        request=request,
        active_item="tables",
    )
