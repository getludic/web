from collections.abc import Callable
from typing import override

from ludic.attrs import GlobalAttrs
from ludic.catalog.headers import H1
from ludic.catalog.typography import CodeBlock, Paragraph
from ludic.html import b, div, style
from ludic.styles.types import SizeClamp
from ludic.types import Component
from ludic.web import LudicApp, Request
from starlette.responses import FileResponse

from web import config
from web.pages import HomePage

app = LudicApp(debug=config.DEBUG)


class CodeSample(Component[str, GlobalAttrs]):
    classes = ["code-sample"]
    styles = style.use(
        lambda theme: {
            ".code-sample .code-block": {
                "display": "inline-block",
                "text-align": "left",
                "max-width": "42rem",
                "padding": theme.sizes.xl,
                "border-radius": theme.rounding.more,
                "border": f"1px solid {theme.colors.light.darken(2)}",
                "margin": "auto",
            },
            ".code-sample": {
                "display": "flex",  # type: ignore
                "justify-content": "center",  # type: ignore
                "min-height": "30rem",  # type: ignore
                "view-transition-name": "slide-it",  # type: ignore
            },
            "@keyframes fade-in": {"from": {"opacity": "0"}},
            "@keyframes fade-out": {"to": {"opacity": "0"}},
            "@keyframes slide-from-right": {"from": {"transform": "translateX(90px)"}},
            "@keyframes slide-to-left": {"to": {"transform": "translateX(-90px)"}},
            "::view-transition-old(slide-it)": {
                "animation": (
                    "180ms cubic-bezier(0.4, 0, 1, 1) both fade-out,"
                    "600ms cubic-bezier(0.4, 0, 0.2, 1) both slide-to-left"
                ),
            },
            "::view-transition-new(slide-it)": {
                "animation": (
                    "420ms cubic-bezier(0, 0, 0.2, 1) 90ms both fade-in,"
                    "600ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-right"
                ),
            },
        }
    )

    @override
    def render(self) -> div:
        return div(
            CodeBlock(*self.children, language="python"),
            **self.attrs,
        )


@app.get("/")
def index(request: Request) -> HomePage:
    return HomePage(
        H1(
            "Ludic Framework",
            style={"font-size": SizeClamp(2.5, 3, 8)},
        ),
        Paragraph(
            f"Build Interactive {b("Web Apps in Pure Python")} in Minutes",
            style={"font-size": request.state.theme.headers.h4.size * 0.8},
        ),
        code_sample(request, 0),
        request=request,
    )


@app.get("/code-samples/{id:int}")
def code_sample(request: Request, id: int) -> CodeSample:
    samples: list[Callable[[GlobalAttrs], CodeSample]] = [
        lambda attributes: CodeSample(
            '''
            from ludic.catalog.layouts import Box
            from ludic.catalog.typography import Link
            from ludic.web import LudicApp

            app = LudicApp()

            @app.get("/")
            async def index() -> Box:
                """Homepage endpoint greeting visitors."""
                return Box(
                    f"Welcome to {Link("Ludic", to="/")}!",
                )
            ''',
            **attributes,
        ),
        lambda attributes: CodeSample(
            '''
            class LinkAttrs(Attrs):
                to: str

            class Link(Component[str, LinkAttrs]):
                """Custom styled Link component."""

                @override
                def render(self) -> a:
                    return a(
                        *self.children,
                        href=self.attrs["to"],
                        style={"color": self.theme.colors.primary},
                    )
            ''',
            **attributes,
        ),
        lambda attributes: CodeSample(
            '''
            @app.get("/counter/{num:int}")
            def counter(num: int) -> Cluster:
                """Simple counter endpoint."""
                return Cluster(
                    ButtonDanger(
                        "Decrement",
                        hx_get=app.url_path_for("counter", num=num - 1),
                        hx_target="#counter",
                    ),
                    b(num, style={"font-size": "2em"}),
                    ButtonSuccess(
                        "Increment",
                        hx_get=app.url_path_for("counter", num=num + 1),
                        hx_target="#counter",
                    ),
                    id="counter",
                )
            ''',
            **attributes,
        ),
        lambda attributes: CodeSample(
            '''
            class SearchBar(Component[NoChildren, GlobalAttrs]):
                """Custom search bar component."""
                classes = ["search-bar"]
                styles = style.use(lambda theme: {
                    ".search-bar input": {
                        "border": f"1px solid {theme.colors.light}",
                        "color": theme.colors.dark,
                    },
                })

                @override
                def render(self) -> InputField:
                    return InputField(type="search", **self.attrs)
            ''',
            **attributes,
        ),
    ]
    attrs: GlobalAttrs = {
        "hx_get": request.url_for(
            "code_sample", id=id + 1 if id < len(samples) - 1 else 0
        ).path,
        "hx_trigger": "load delay:10s",
        "hx_swap": "outerHTML transition:true",
    }
    try:
        return samples[id](attrs)
    except IndexError:
        return samples[0](attrs)


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("static/favicon.ico")
