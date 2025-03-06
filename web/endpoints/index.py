from typing import override

from ludic import Attrs, Component
from ludic.catalog.buttons import ButtonSecondary
from ludic.catalog.headers import H1
from ludic.catalog.layouts import Cluster, Stack
from ludic.catalog.typography import CodeBlock, Paragraph
from ludic.html import b, style
from ludic.styles.types import SizeClamp
from ludic.web import LudicApp, Request
from starlette.responses import FileResponse

from web import config
from web.pages import HomePage

app = LudicApp(debug=config.DEBUG)


SAMPLES: list[str] = [
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
    '''
    class MyLayout(Component[AnyChildren, GlobalAttrs]):
        """A simple layout for my website."""

        @override
        def render(self) -> WithSidebar:
            return WithSidebar(
                Center(*self.children, **self.attrs),
                Sidebar(
                    Cluster(
                        Button("Menu Item 1"),
                        Button("Menu Item 2"),
                        Button("Menu Item 3"),
                    ),
                ),
            )
    ''',
    """
    from ludic.catalog.headers import H1
    from ludic.catalog.typography import Code, Paragraph
    from ludic.html import b

    from .pages import Page

    def index() -> Page:
        return Page(
            H1("HTML Page in Pure Python"),
            Paragraph(
                f"A sample on how to use {b("Ludic")} to build"
                f"static {Code("HTML")} page in pure Python."
            ),
        )
    """,
]


class CodeSampleAttrs(Attrs):
    sample_url: str


class CodeSample(Component[str, CodeSampleAttrs]):
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
                "margin-inline": "auto",
                "font-size": theme.sizes.s,
            },
            ".code-sample": {
                "display": "flex",
                "justify-content": "center",
                "view-transition-name": "slide-it",
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
    def render(self) -> Stack:
        return Stack(
            CodeBlock(*self.children, language="python"),
            Cluster(
                ButtonSecondary(
                    "Next Sample",
                    hx_get=self.attrs["sample_url"],
                    hx_target="#code-sample",
                    hx_swap="outerHTML transition:true",
                ),
                classes=["justify-center"],
            ),
            id="code-sample",
        )


@app.get("/")
def index(request: Request) -> HomePage:
    return HomePage(
        H1(
            "Ludic Framework",
            style={"font-size": SizeClamp(2.5, 3, 8)},
        ),
        Paragraph(
            f"Web Development in {b("Pure Python")} with {b("Type-Guided")} Components",
            style={"font-size": request.state.theme.headers.h4.size * 0.8},
        ),
        code_sample(request, 0),
        request=request,
    )


@app.get("/code-samples/{id:int}")
def code_sample(request: Request, id: int) -> CodeSample:
    sample_url = request.url_for(
        "code_sample", id=id + 1 if id < len(SAMPLES) - 1 else 0
    ).path
    samples: list[CodeSample] = [
        CodeSample(sample, sample_url=sample_url) for sample in SAMPLES
    ]
    return samples[id] if len(samples) > id else samples[0]


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("static/favicon.ico")


@app.get("/robots.txt")
def robots() -> FileResponse:
    return FileResponse("static/robots.txt")
