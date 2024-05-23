from typing import override

from ludic.catalog.headers import H1
from ludic.catalog.typography import CodeBlock, Paragraph
from ludic.html import b, style
from ludic.types import Component, NoAttrs, NoChildren
from ludic.web import LudicApp, Request

from web.pages import HomePage

app = LudicApp(debug=True)


class CodeSample(Component[NoChildren, NoAttrs]):
    classes = ["code-sample"]
    styles = style.use(
        lambda theme: {
            ".code-sample": {
                "text-align": "left",
                "margin-inline": "auto",
                "width": "auto",
                "padding": theme.sizes.xxl,
                "border-radius": theme.rounding.more,
                "border": f"1px solid {theme.colors.light.darken(2)}",
            }
        }
    )

    @override
    def render(self) -> CodeBlock:
        return CodeBlock(
            """
            app = LudicApp()

            @app.get("/")
            async def homepage() -> Box:
                return Box(
                    f"Welcome to {Link("Ludic", to="/")}!"
                )
            """,
            language="python",
        )


@app.get("/")
def index(request: Request) -> HomePage:
    return HomePage(
        H1("Ludic Framework", style={"font-size": "5rem"}),
        Paragraph(
            f"Build Dynamic {b("Web Apps in Pure Python")} in Minutes",
            style={"font-size": "1.5rem"},
        ),
        CodeSample(),
        request=request,
    )
