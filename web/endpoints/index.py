from typing import override

from ludic.catalog.headers import H1
from ludic.catalog.typography import CodeBlock, Paragraph
from ludic.html import b, style
from ludic.styles.types import SizeClamp
from ludic.types import Component, NoAttrs
from ludic.web import LudicApp, Request
from starlette.responses import FileResponse

from web import config
from web.pages import HomePage

app = LudicApp(debug=config.DEBUG)


class CodeSample(Component[str, NoAttrs]):
    classes = ["code-sample"]
    styles = style.use(
        lambda theme: {
            ".code-sample": {
                "text-align": "left",
                "margin-inline": "auto",
                "max-width": "33rem",
                "padding": theme.sizes.xl,
                "border-radius": theme.rounding.more,
                "border": f"1px solid {theme.colors.light.darken(2)}",
            }
        }
    )

    @override
    def render(self) -> CodeBlock:
        return CodeBlock(*self.children, language="python")


@app.get("/")
def index(request: Request) -> HomePage:
    return HomePage(
        H1(
            "Ludic Framework",
            style={"font-size": SizeClamp(2, 5, 6)},
        ),
        Paragraph(
            f"Build Interactive {b("Web Apps in Pure Python")} in Minutes",
            style={"font-size": request.state.theme.headers.h4.size},
        ),
        CodeSample(
            """
            app = LudicApp()

            @app.get("/")
            async def homepage() -> Box:
                return Box(
                    f"Welcome to {Link("Ludic", to="/")}!"
                )
            """
        ),
        request=request,
    )


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("static/favicon.ico")
