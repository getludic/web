from ludic.catalog.headers import H1
from ludic.web import LudicApp, Request

from web.pages import PageWithMenu

app = LudicApp()


@app.get("/styles/")
def styles(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Styles"),
        request=request,
        active_item="styles",
    )
