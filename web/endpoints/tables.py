from ludic.catalog.headers import H1
from ludic.web import LudicApp, Request

from web.pages import PageWithMenu

app = LudicApp()


@app.get("/tables/")
def tables(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Tables"),
        request=request,
        active_item="tables",
    )
