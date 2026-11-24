from typing import NotRequired, override

from ludic import Attrs, Component
from ludic.catalog.buttons import ButtonLink
from ludic.catalog.cards import Card
from ludic.catalog.layouts import Box, Cluster, Grid
from ludic.catalog.tabs import Tab, Tabs
from ludic.catalog.typography import Code, CodeBlock, Link
from ludic.html import a, b, div, h1, h2, h3, p, section, span, style
from ludic.types import AnyChildren
from ludic.web import LudicApp, Request
from starlette.responses import FileResponse

from web import config
from web.components import Quote
from web.endpoints.docs.index import Counter
from web.pages import HomePage

app = LudicApp(debug=config.DEBUG)


class HeroLinkAttrs(Attrs):
    to: str


class HeroLink(Component[str, HeroLinkAttrs]):
    """The component from the hero code sample, rendered live below it."""

    @override
    def render(self) -> a:
        return a(*self.children, href=self.attrs["to"])


HERO_CODE = """
from typing import override

from ludic import Attrs, Component
from ludic.html import a, b, p

class LinkAttrs(Attrs):
    to: str

class Link(Component[str, LinkAttrs]):
    @override
    def render(self) -> a:
        return a(*self.children, href=self.attrs["to"])

p(t"Hello {b('Stranger')}! Click {Link('here', to='/docs/')}.")
"""

INVALID_CODE = """
br("Hello, World!")
html(body())
div("Test", href="test")
Link("here", too="/home")
Link(div("here"), to="/home")
Link("here")
"""

MYPY_OUTPUT = """
app.py:1: error: Argument 1 to "br" has incompatible type "str"; expected "Never"
app.py:2: error: Argument 1 to "html" has incompatible type "body"; expected "head"
app.py:3: error: Unexpected keyword argument "href" for "div"
app.py:4: error: Unexpected keyword argument "too" for "Link"; did you mean "to"?
app.py:5: error: Argument 1 to "Link" has incompatible type "div"; expected "str"
app.py:6: error: Missing named argument "to" for "Link"
Found 6 errors in 1 file (checked 1 source file)
"""

FRAMEWORKS: list[tuple[str, str, str]] = [
    (
        "Starlette",
        "app.py",
        """
        from ludic.html import b, p
        from ludic.web import LudicApp

        app = LudicApp()


        @app.get("/")
        async def homepage() -> p:
            return p(t"Hello {b('Stranger')}!")
        """,
    ),
    (
        "FastAPI",
        "main.py",
        """
        from fastapi import FastAPI

        from ludic.contrib.fastapi import LudicRoute
        from ludic.html import p

        app = FastAPI()
        app.router.route_class = LudicRoute


        @app.get("/")
        async def homepage() -> p:
            return p("Hello, World!")
        """,
    ),
    (
        "Django",
        "views.py",
        """
        from django.http import HttpRequest

        from ludic.contrib.django import LudicResponse
        from ludic.html import p


        def index(request: HttpRequest) -> LudicResponse:
            return LudicResponse(p("Hello, World!"))
        """,
    ),
    (
        "Anything else",
        "render.py",
        """
        from ludic.html import b, p

        html = p(t"Hello {b('World')}!").to_html()
        # '<p>Hello <b>World</b>!</p>'
        """,
    ),
]

COUNTER_CODE = """
class Counter(Endpoint[CounterAttrs]):
    @classmethod
    def get(cls, number: int) -> Self:
        return cls(number=number)

    @override
    def render(self) -> Cluster:
        number = self.attrs["number"]
        return Cluster(
            ButtonDanger(
                "Decrement",
                disabled=number <= 0,
                hx_get=self.url_for(Counter, number=number - 1).path,
                hx_target="#counter",
            ),
            b(number),
            ButtonSuccess(
                "Increment",
                hx_get=self.url_for(Counter, number=number + 1).path,
                hx_target="#counter",
            ),
            id="counter",
        )
"""

FEATURES: list[tuple[str, str, str]] = [
    (
        "✓",
        "Type-guided HTML",
        "Every element knows which children and attributes it allows, so mypy "
        "catches invalid markup.",
    ),
    (
        "</>",
        "Components",
        "Compose pages from small Python classes, like in React, with typed "
        "children and attributes.",
    ),
    (
        't""',
        "t-strings",
        "Mix text and elements with Python 3.14 template strings, no template "
        "language needed.",
    ),
    (
        "<",
        "Escaped by default",
        "Text is always escaped. Trusted markup is marked explicitly with Safe.",
    ),
    (
        "hx-",
        "htmx attributes",
        "Typed hx-* attributes make dynamic pages with almost no JavaScript.",
    ),
    (
        "{}",
        "Any framework",
        "Use the Starlette based web framework, FastAPI, Django, or just call "
        ".to_html().",
    ),
    (
        "◐",
        "Themes",
        "Components declare their CSS and read colors and sizes from the theme. "
        "This site's dark mode is a second theme.",
    ),
    (
        "▦",
        "Layouts",
        "Responsive layouts adopted from the Every Layout book, ready in the catalog.",
    ),
]


class SectionAttrs(Attrs):
    eyebrow: str
    title: str
    lead: NotRequired[AnyChildren]
    id: NotRequired[str]
    classes: NotRequired[list[str]]


class HomeSection(Component[AnyChildren, SectionAttrs]):
    """A section of the homepage with a small label, a title and a lead."""

    classes = ["home-section"]
    styles = style.use(
        lambda theme: {
            "section.home-section": {
                "padding-block": theme.sizes.xxxxl * 1.6,
            },
            "section.home-section.tinted": {
                "border-block": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                ),
                "background-color": theme.colors.light.lighten(1),
            },
            ".home-section > .section-content": {
                "max-inline-size": "72rem",
                "margin-inline": "auto",
                "padding-inline": theme.sizes.l,
            },
            ".home-section .section-header": {
                "max-inline-size": "44rem",
                "margin-block-end": theme.sizes.xxl,
            },
            ".home-section .eyebrow": {
                "color": theme.colors.primary.darken(1),
                "font-size": theme.fonts.size * 0.8,
                "font-weight": "700",
                "letter-spacing": "0.08em",
                "text-transform": "uppercase",
            },
            ".home-section .section-header h2": {
                "margin-block-start": theme.sizes.xxs,
                "font-size": "clamp(1.9rem, 1.4rem + 1.8vw, 2.75rem)",
                "line-height": 1.15,
            },
            ".home-section .section-header .lead": {
                "margin-block-start": theme.sizes.s,
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 1.1,
            },
        }
    )

    @override
    def render(self) -> section:
        header = [
            p(self.attrs["eyebrow"], classes=["eyebrow"]),
            h2(self.attrs["title"]),
        ]
        if lead := self.attrs.get("lead"):
            header.append(p(lead, classes=["lead"]))
        return section(
            div(
                div(*header, classes=["section-header"]),
                *self.children,
                classes=["section-content"],
            ),
            **self.attrs_for(section),
        )


class Hero(Component[AnyChildren, Attrs]):
    classes = ["hero"]
    styles = style.use(
        lambda theme: {
            "section.hero": {
                "padding-block": f"{theme.sizes.xxxxl * 1.4} {theme.sizes.xxxxl}",
                "background-image": (
                    "radial-gradient(60rem 30rem at 80% -10%, "
                    f"{theme.colors.primary.lighten(1)}, transparent 70%)"
                ),
            },
            ".hero > .hero-content": {
                "display": "grid",
                "grid-template-columns": "minmax(0, 1fr) minmax(0, 1.1fr)",
                "gap": theme.sizes.xxxl,
                "align-items": "center",
                "max-inline-size": "72rem",
                "margin-inline": "auto",
                "padding-inline": theme.sizes.l,
            },
            ".hero a.badge": {
                "display": "inline-block",
                "padding": f"{theme.sizes.xxxxs} {theme.sizes.s}",
                "border": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                ),
                "border-radius": "999px",
                "background-color": theme.colors.white,
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.85,
                "font-weight": "500",
            },
            ".hero a.badge:hover": {
                "border-color": theme.colors.primary,
                "text-decoration": "none",
            },
            ".hero h1": {
                "margin-block-start": theme.sizes.m,
                "font-size": "clamp(2.5rem, 1.6rem + 3.6vw, 4.25rem)",
                "line-height": 1.05,
            },
            ".hero h1 .accent": {
                "color": theme.colors.primary,
            },
            ".hero .lead": {
                "margin-block-start": theme.sizes.l,
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 1.2,
            },
            ".hero .cluster": {
                "margin-block-start": theme.sizes.xl,
            },
            ".hero .install": {
                "max-inline-size": "22rem",
                "margin-block-start": theme.sizes.l,
            },
            ".hero .hero-demo > * + *": {
                "margin-block-start": theme.sizes.s,
            },
            ".hero .result": {
                "padding": f"{theme.sizes.s} {theme.sizes.l}",
                "border": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                ),
                "border-radius": theme.rounding.normal,
                "background-color": theme.colors.white,
            },
            ".hero .result-label": {
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.75,
                "font-weight": "600",
                "letter-spacing": "0.06em",
                "text-transform": "uppercase",
            },
            "@media (max-width: 60rem)": {
                ".hero > .hero-content": {
                    "grid-template-columns": "minmax(0, 1fr)",
                },
            },
        }
    )

    @override
    def render(self) -> section:
        return section(div(*self.children, classes=["hero-content"]))


class FeatureIcon(Component[str, Attrs]):
    classes = ["feature-icon"]
    styles = style.use(
        lambda theme: {
            ".feature-icon": {
                "display": "inline-grid",
                "place-items": "center",
                "inline-size": "2.5rem",
                "block-size": "2.5rem",
                "border-radius": theme.rounding.normal,
                "background-color": theme.colors.primary.lighten(1),
                "color": theme.colors.primary.darken(1),
                "font-family": theme.fonts.monospace,
                "font-size": theme.fonts.size * 0.9,
                "font-weight": "700",
            },
            ".home-section .card h3": {
                "font-size": theme.fonts.size * 1.1,
                "letter-spacing": "-0.01em",
            },
            ".home-section .card p": {
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.95,
            },
        }
    )

    @override
    def render(self) -> span:
        return span(*self.children, aria_hidden="true")


class TwoColumns(Component[AnyChildren, Attrs]):
    classes = ["two-columns"]
    styles = style.use(
        lambda theme: {
            ".home .code-block.wrap pre": {
                "white-space": "pre-wrap",
                "overflow-wrap": "anywhere",
            },
            ".two-columns": {
                "display": "grid",
                "grid-template-columns": (
                    "repeat(auto-fit, minmax(min(26rem, 100%), 1fr))"
                ),
                "gap": theme.sizes.xl,
                "align-items": "stretch",
            },
        }
    )

    @override
    def render(self) -> div:
        return div(*self.children)


class DemoPanel(Component[AnyChildren, Attrs]):
    classes = ["demo-panel"]
    styles = style.use(
        lambda theme: {
            ".demo-panel": {
                "display": "flex",
                "flex-direction": "column",
                "gap": theme.sizes.m,
                "justify-content": "center",
                "align-items": "center",
                "padding": theme.sizes.xl,
                "border": (
                    f"{theme.borders.thin} dashed {theme.colors.light.darken(2)}"
                ),
                "border-radius": theme.rounding.more,
                "text-align": "center",
            },
            ".demo-panel .demo-note": {
                "max-inline-size": "32ch",
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.9,
            },
        }
    )

    @override
    def render(self) -> div:
        return div(*self.children)


@app.get("/")
def index(request: Request) -> HomePage:
    docs_url = request.url_for("docs:index").path
    hero_result = p(t"Hello {b('Stranger')}! Click {HeroLink('here', to=docs_url)}.")
    accent = span("pure Python", classes=["accent"])

    return HomePage(
        Hero(
            div(
                a(
                    "Ludic 1.0: t-strings for Python 3.14 →",
                    href=request.url_for("docs:components").path,
                    classes=["badge"],
                ),
                h1(t"Typed HTML components in {accent}"),
                p(
                    "Write HTML as Python components. Your type checker validates "
                    "the markup, so wrong nesting, unknown attributes and missing "
                    "arguments fail before a page ever renders.",
                    classes=["lead"],
                ),
                Cluster(
                    ButtonLink(
                        "Get started",
                        to=request.url_for("docs:getting_started").path,
                        classes=["primary", "large"],
                    ),
                    ButtonLink(
                        "Star on GitHub",
                        to=config.GITHUB_REPO_URL,
                        classes=["large"],
                    ),
                    classes=["small"],
                ),
                CodeBlock("pip install ludic", copy_button=True, classes=["install"]),
            ),
            div(
                CodeBlock(
                    HERO_CODE,
                    language="python",
                    label="components.py",
                    copy_button=True,
                ),
                div(
                    p("Rendered by this page", classes=["result-label"]),
                    hero_result,
                    classes=["result"],
                ),
                CodeBlock(hero_result.to_html(), language="html", label="HTML"),
                classes=["hero-demo"],
            ),
        ),
        HomeSection(
            TwoColumns(
                CodeBlock(INVALID_CODE, language="python", label="app.py"),
                CodeBlock(MYPY_OUTPUT, label="$ mypy app.py", classes=["wrap"]),
            ),
            eyebrow="Type checking",
            title="Invalid markup is a type error",
            lead=(
                "Elements and components declare the children and attributes they "
                "accept. The mypy plugin checks every call, so mistakes show up in "
                "your editor and in CI instead of in the browser."
            ),
            classes=["tinted"],
        ),
        HomeSection(
            Grid(
                *(
                    Card(FeatureIcon(icon), h3(title), p(text))
                    for icon, title, text in FEATURES
                ),
            ),
            eyebrow="Features",
            title="Everything you need to render HTML, nothing more",
            lead=(
                "At its core Ludic only renders HTML, so it fits into the web "
                "framework you already use."
            ),
        ),
        HomeSection(
            Tabs(
                *(
                    Tab(
                        CodeBlock(code, language="python", label=label),
                        label=name,
                    )
                    for name, label, code in FRAMEWORKS
                ),
                id="frameworks",
            ),
            eyebrow="Integrations",
            title="Use it with your framework",
            lead=t"Return elements from Starlette, FastAPI or Django views, or "
            t"render a string with {Code('.to_html()')} anywhere else.",
            classes=["tinted"],
        ),
        HomeSection(
            TwoColumns(
                CodeBlock(COUNTER_CODE, language="python", label="counter.py"),
                DemoPanel(
                    Box(Counter(number=0)),
                    p(
                        "This counter is the endpoint on the left. Each click asks "
                        "the server for the new HTML and htmx swaps it in.",
                        classes=["demo-note"],
                    ),
                ),
            ),
            eyebrow="htmx",
            title="Interactive pages without writing JavaScript",
            lead=(
                "Endpoints render themselves as components, and typed hx-* "
                "attributes wire them together."
            ),
        ),
        HomeSection(
            TwoColumns(
                Card(
                    h3("Agent skills"),
                    p("Teach any coding agent to write idiomatic Ludic code."),
                    CodeBlock(
                        "npx skills add https://github.com/getludic/ludic --skill '*'",
                        copy_button=True,
                        classes=["wrap"],
                    ),
                ),
                Card(
                    h3("Claude Code plugin"),
                    p("Install both skills from the Ludic plugin marketplace."),
                    CodeBlock(
                        "/plugin marketplace add getludic/ludic\n"
                        "/plugin install ludic@ludic",
                        copy_button=True,
                    ),
                ),
                Card(
                    h3("Context7"),
                    p(
                        t"Agents that look up docs with Context7 get the Ludic "
                        t"docs and rules from {Code('/getludic/ludic')}."
                    ),
                    Link(
                        "Open on Context7 →", to="https://context7.com/getludic/ludic"
                    ),
                ),
                Card(
                    h3("llms.txt"),
                    p(
                        "Every page of this site has a Markdown version, listed "
                        "in llms.txt, or all in one file."
                    ),
                    Cluster(
                        a("llms.txt", href=request.url_for("llms_txt").path),
                        a(
                            "llms-full.txt",
                            href=request.url_for("llms_full_txt").path,
                        ),
                        classes=["small"],
                    ),
                ),
            ),
            eyebrow="AI tooling",
            title="Built for coding agents",
            lead=(
                "Most code is now written with an AI assistant. Ludic ships "
                "instructions for agents, so they write type-safe Ludic code "
                "and check it with mypy."
            ),
            id="agents",
            classes=["tinted"],
        ),
        HomeSection(
            Quote(
                "I've just composed my first PageLayout component and I have no words!",
                source="Igor Davydenko",
            ),
            eyebrow="From the community",
            title="Loved by Python developers",
        ),
        HomeSection(
            Cluster(
                ButtonLink(
                    "Read the docs",
                    to=docs_url,
                    classes=["primary", "large"],
                ),
                ButtonLink(
                    "Browse the catalog",
                    to=request.url_for("catalog:index").path,
                    classes=["large"],
                ),
                ButtonLink(
                    "See examples",
                    to=request.url_for("examples:index").path,
                    classes=["large"],
                ),
                classes=["small"],
            ),
            eyebrow="Get started",
            title="Build your next page with Ludic",
            lead=t"Install it with {Code('pip install ludic')} and follow the guide.",
            classes=["tinted"],
        ),
        request=request,
    )


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("static/favicon.ico")
