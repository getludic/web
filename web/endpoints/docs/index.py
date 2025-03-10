from typing import Self, override

from ludic import Blank
from ludic.attrs import Attrs
from ludic.catalog.buttons import ButtonDanger, ButtonSuccess
from ludic.catalog.headers import H1, H2
from ludic.catalog.layouts import Box, Cluster
from ludic.catalog.lists import Item, List
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b
from ludic.web import Endpoint, Request

from web import config
from web.components import Badge, LogoBig, Quote
from web.pages import Page


def index(request: Request) -> Page:
    return Page(
        LogoBig(logo_url=str(request.url_for("static", path="ludic.png"))),
        Cluster(
            Badge(
                url="https://github.com/getludic/ludic/actions",
                img_url="https://github.com/getludic/ludic/actions/workflows/test.yaml/badge.svg",
                title="Tests Status",
            ),
            Badge(
                url="https://codecov.io/gh/getludic/ludic",
                img_url="https://codecov.io/gh/getludic/ludic/graph/badge.svg?token=BBDNJWHMGX",
                title="Code Coverage",
            ),
            Badge(
                url="https://www.python.org/downloads/release/python-3130/",
                img_url="https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg",
                title="Python 3.12 and 3.13",
            ),
            Badge(
                url="https://mypy-lang.org/",
                img_url="https://www.mypy-lang.org/static/mypy_badge.svg",
                title="Checked with mypy",
            ),
            Badge(
                url=config.DISCORD_INVITE_URL,
                img_url="https://img.shields.io/badge/discord-ludic-black",
                title="Discord Server",
            ),
            classes=["small"],
        ),
        H1("Introduction"),
        Quote(
            "I've just composed my first PageLayout component and I have no words!",
            source="Igor Davydenko",
        ),
        Paragraph(
            "Ludic is a lightweight framework for building HTML pages with a component "
            f"approach similar to {Link('React', to='https://react.dev/')}. It is "
            f"built to be used together with {
                Link('htmx.org', to='https://htmx.org/')
            } so that developers don't need "
            "to write almost any JavaScript to create dynamic web services. Its "
            "potential can be leveraged together with its web framework which is a "
            f"wrapper around the powerful {
                Link('Starlette', to='https://www.starlette.io/')
            } framework. It is built "
            "with the latest Python 3.12 features heavily incorporating typing."
        ),
        H2("Features"),
        List(
            Item(
                f"Seamless {b('</> htmx')} integration for rapid web development "
                f"in {b('pure Python')}"
            ),
            Item(f"{b('Type-Guided components')} utilizing Python's typing system"),
            Item(
                f"Uses the power of {b('Starlette')} and {b('Async')} for "
                "high-performance web development"
            ),
            Item(f"Build HTML with the ease and power of Python {b('f-strings')}"),
            Item(f"Add CSS styling to your components with {b('Themes')}"),
            Item(
                "Create simple, responsive layouts adopted from the "
                f"{b('Every Layout Book')}"
            ),
        ),
        H2("Comparison"),
        Paragraph("Here is a table comparing Ludic to other similar tools:"),
        Table(
            TableHead(
                "Feature",
                "Ludic",
                "FastUI",
                "Reflex",
            ),
            TableRow(
                "HTML rendering",
                "Server Side",
                "Client Side",
                "Client Side",
            ),
            TableRow(
                "Uses a template engine",
                "No",
                "No",
                "No",
            ),
            TableRow(
                "UI interactivity",
                Blank(Link("</> htmx", to="https://htmx.org"), "*"),
                Link("React", to="https://react.dev"),
                Link("React", to="https://react.dev"),
            ),
            TableRow(
                "Backend framework",
                Blank(
                    Link("Starlette", to="https://www.starlette.io/"),
                    ", ",
                    Link("FastAPI", to="https://fastapi.tiangolo.com/"),
                    ", ",
                    Link("Django", to="https://www.djangoproject.com/"),
                    "*",
                ),
                Link("FastAPI", to="https://fastapi.tiangolo.com/"),
                Link("FastAPI", to="https://fastapi.tiangolo.com/"),
            ),
            TableRow(
                "Client-Server Communication",
                Link(
                    "HTML + REST",
                    to="https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/",
                ),
                Link(
                    "JSON + REST",
                    to="https://github.com/pydantic/FastUI?tab=readme-ov-file#the-principle-long-version",
                ),
                Link(
                    "WebSockets",
                    to="https://reflex.dev/blog/2024-03-21-reflex-architecture/",
                ),
            ),
        ),
        Paragraph(
            "(*) HTMX as well as Starlette or Django are optional dependencies for "
            "Ludic, it does not enforce any frontend or backend frameworks. At it's "
            "core, Ludic only generates HTML and allows registering CSS.",
            style={"font-size": "0.8em"},
        ),
        H2("Quick Example"),
        Paragraph(
            "Here is a simple re-implementation of an example from "
            f"{
                Link(
                    'Reflex',
                    to=(
                        'https://reflex.dev/docs/getting-started/introduction/'
                        '#an-example:-make-it-count'
                    ),
                )
            } (although only for natural numbers):"
        ),
        Box(Counter(number=0)),
        Paragraph("The counter can be included on any page like here:"),
        CodeBlock(
            """
            from typing import override

            from ludic.html import b
            from ludic.web import Endpoint, LudicApp, Request
            from ludic.catalog.buttons import ButtonDanger, ButtonSuccess
            from ludic.catalog.layouts import Box, Cluster

            app = LudicApp()

            @app.get("/")
            def index(request: Request) -> Box:
                return Box(Counter(0))
            """,
            language="python",
        ),
        Paragraph(
            f"Note that the {Code('Box')} is just a component wrapping the buttons "
            f"and the number to make it nicely framed. You can read more about the "
            f"{Code('Box')} in the {
                b(Link('Layouts', to=(request.url_for('catalog:layouts').path)))
            } section later. Anyway, the {Code('Counter')} component is the part "
            "that is more interesting: "
        ),
        CodeBlock(
            """
            @app.get("/counter/{number:int}")
            def Counter(number: int) -> Cluster:
                return Cluster(
                    ButtonDanger(
                        "Decrement",
                        disabled=number <= 0
                        hx_get=app.url_path_for("Counter", number=max(0, number - 1)),
                        hx_target="#counter",
                    ),
                    b(number, style={"font-size": "2em"}),
                    ButtonSuccess(
                        "Increment",
                        hx_get=app.url_path_for("Counter", number=number + 1),
                        hx_target="#counter",
                    ),
                    id="counter",
                )
            """,
            language="python",
        ),
        H2("Requirements"),
        Paragraph("Python 3.12+"),
        H2("Installation"),
        Paragraph(
            "The following command installs Ludic with Starlette as ASGI framework. "
            f"If you want to use FastAPI or Django, check the {
                Link(
                    'Other Integrations guide',
                    to=request.url_path_for("docs:web_framework"),
                )
            }:"
        ),
        CodeBlock('pip install "ludic[full]"'),
        Paragraph(
            f"You can also use the {
                Link('cookiecutter', to='https://github.com/cookiecutter/cookiecutter')
            } "
            f"template to quickly create a new project, using {
                Link('UV', to='https://docs.astral.sh/uv/')
            } you can do that with only one "
            "command:"
        ),
        CodeBlock("uvx cookiecutter gh:getludic/template"),
        Paragraph(
            "For more information on how to get started, check the ",
            Link(
                "Getting Started guide", to=request.url_path_for("docs:getting_started")
            ),
            ".",
        ),
        H2("Integrations"),
        Paragraph(
            "Here is a list of integrations and a link to the guide on how to get "
            "started:",
        ),
        List(
            Link("Starlette", to=f"{request.url_path_for('docs:web_framework')}"),
            Link("FastAPI", to=f"{request.url_path_for('docs:integrations')}#fastapi"),
            Link("Django", to=f"{request.url_path_for('docs:integrations')}#django"),
        ),
        H2("Contributing"),
        Paragraph(
            "Any contributions to the framework are warmly welcome! Your help will "
            "make it a better resource for the community. If you're ready to "
            "contribute, read the ",
            Link(
                "contribution guide on GitHub",
                to=f"{config.GITHUB_REPO_URL}/blob/main/CONTRIBUTING.md",
            ),
            ".",
        ),
        List(
            Item(
                Link("GitHub Issues", to=f"{config.GITHUB_REPO_URL}/issues"),
                " – If you encounter a bug, please report it here.",
            ),
            Item(
                Link(
                    "GitHub Discussions",
                    to=f"{config.GITHUB_REPO_URL}/discussions",
                ),
                " – To request a new feature, this is the best place to initiate the "
                "discussion.",
            ),
            Item(
                Link("Discord", to="https://discord.gg/4Y5fSQUS"),
                " – Join our Discord server for support, sharing ideas, and receiving "
                "assistance.",
            ),
        ),
        request=request,
        active_item="docs:index",
        title="Ludic - Documentation",
    )


class CounterAttrs(Attrs):
    number: int


class Counter(Endpoint[CounterAttrs]):
    @classmethod
    def get(cls, number: int) -> Self:
        return cls(number=number)

    @override
    def render(self) -> Cluster:
        return Cluster(
            ButtonDanger(
                "Decrement",
                disabled=self.attrs["number"] <= 0,
                hx_get=self.url_for(
                    "docs:Counter", number=max(0, self.attrs["number"] - 1)
                ),
                hx_target="#counter",
                hx_disabled_elt="this",
            ),
            b(
                self.attrs["number"],
                style={"font-size": self.theme.fonts.size * 2},
            ),
            ButtonSuccess(
                "Increment",
                hx_get=self.url_for("docs:Counter", number=self.attrs["number"] + 1),
                hx_target="#counter",
                hx_disabled_elt="this",
            ),
            id="counter",
            classes=["centered"],
        )
