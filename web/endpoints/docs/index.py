from typing import Self, override

from ludic.attrs import Attrs
from ludic.catalog.buttons import ButtonDanger, ButtonSuccess
from ludic.catalog.headers import H1, H2, H3
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
                url="https://www.python.org/downloads/release/python-3140/",
                img_url="https://img.shields.io/badge/Python-3.14%2B-blue.svg",
                title="Python 3.14+",
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
            "Ludic lets you write HTML as typed Python components. Your type checker "
            "validates the markup, so wrong nesting, unknown attributes and missing "
            "arguments are caught before a page ever renders. At its core Ludic only "
            "renders HTML, so it fits into the web framework you already use, and it "
            f"pairs naturally with {Link('htmx', to='https://htmx.org/')}."
        ),
        CodeBlock(
            """
            from typing import override

            from ludic import Attrs, Component
            from ludic.html import a, b, p


            class LinkAttrs(Attrs):
                to: str


            class Link(Component[str, LinkAttrs]):
                @override
                def render(self) -> a:
                    return a(*self.children, href=self.attrs["to"])


            p(t"Hello {b('Stranger')}! Click {Link('here', to='/home')}.").to_html()
            # <p>Hello <b>Stranger</b>! Click <a href="/home">here</a>.</p>
            """,
            language="python",
        ),
        Paragraph(
            "Invalid markup is a type error. This is what ",
            Link("mypy", to="https://mypy-lang.org/"),
            " reports:",
        ),
        CodeBlock(
            """
            br("Hello, World!")
            # error: Argument 1 to "br" has incompatible type "str"; expected "Never"

            html(body())
            # error: Argument 1 to "html" has incompatible type "body"; expected "head"

            div("Test", href="test")
            # error: Unexpected keyword argument "href" for "div"

            Link("here", too="/home")
            # error: Unexpected keyword argument "too" for "Link"; did you mean "to"?

            Link(div("here"), to="/home")
            # error: Argument 1 to "Link" has incompatible type "div"; expected "str"

            Link("here")
            # error: Missing named argument "to" for "Link"
            """,
            language="python",
        ),
        H2("Features"),
        List(
            Item(
                f"{b('Type-guided HTML')}: every element knows which children and "
                "attributes it allows"
            ),
            Item(
                f"{b('Components')} in pure Python, composed like in "
                f"{Link('React', to='https://react.dev/')}"
            ),
            Item(
                f"Mix markup and text with Python 3.14 {b('t-strings')} "
                "(template strings)"
            ),
            Item(
                f"Text is {b('escaped by default')}, trusted markup is marked "
                f"explicitly with {Code('Safe')}"
            ),
            Item(
                f"Typed {b('</> htmx')} attributes, so dynamic pages need almost no "
                "JavaScript"
            ),
            Item(
                f"Works with {b('Starlette')}, {b('FastAPI')} and {b('Django')}, or "
                "with no framework at all"
            ),
            Item(f"Typed CSS for your components with {b('Themes')}"),
            Item(
                f"Simple, responsive layouts adopted from the {b('Every Layout Book')}"
            ),
        ),
        H2("Comparison"),
        Paragraph(
            "Here is how Ludic compares to other ways of producing HTML in Python:"
        ),
        Table(
            TableHead(
                "Feature",
                "Ludic",
                Link("htpy", to="https://htpy.dev/"),
                Link("FastHTML", to="https://fastht.ml/"),
                Link("tdom", to="https://github.com/t-strings/tdom"),
                Link("Jinja2", to="https://jinja.palletsprojects.com/"),
            ),
            TableRow(
                "How you write HTML",
                "Python calls and t-strings",
                "Python calls, children in []",
                "Python calls",
                "HTML inside t-strings",
                "Template files",
            ),
            TableRow(
                "Children and attributes type-checked per element",
                "Yes",
                "No",
                "No",
                "No",
                "No",
            ),
            TableRow(
                "Web framework",
                "Optional: Starlette, FastAPI, Django or none",
                "Any",
                "Its own, built on Starlette",
                "Any",
                "Any",
            ),
            TableRow(
                "Python",
                "3.14+ (3.12+ with 0.5.x)",
                "3.10+",
                "3.10+",
                "3.14+",
                "3.7+",
            ),
        ),
        Paragraph("The others are a better fit in some cases:"),
        List(
            Item(
                f"{b('htpy')} supports older Python versions and needs no type "
                "checker plugin."
            ),
            Item(
                f"{b('FastHTML')} is a complete web framework rather than a library "
                "you add to one."
            ),
            Item(
                f"{b('tdom')} lets you write real HTML syntax instead of Python calls."
            ),
            Item(
                f"{b('Jinja2')} keeps templates in files that people who do not write "
                "Python can edit."
            ),
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
        Paragraph("Python 3.14+"),
        Paragraph(
            f"{b('Note')}: Ludic 0.5.x supports Python 3.12+ with f-strings. "
            "For Python 3.12 or 3.13, use Ludic 0.5.x and f-strings instead of "
            "t-strings.",
            style={"font-size": "0.9em", "color": "#666"},
        ),
        H2("Installation"),
        Paragraph("The core package renders HTML and has a single dependency:"),
        CodeBlock("pip install ludic"),
        Paragraph(
            "The following command also installs the web framework built on "
            "Starlette, form parsing and code highlighting. "
            f"If you want to use FastAPI or Django, check the {
                Link(
                    'Other Integrations guide',
                    to=request.url_path_for('docs:integrations'),
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
        H3("Type Checking"),
        Paragraph(
            f"Elements from {Code('ludic.html')} are checked by plain type hints. "
            "To also check the attributes of your own components, enable the mypy "
            f"plugin in {Code('pyproject.toml')}:"
        ),
        CodeBlock(
            """
            [tool.mypy]
            plugins = ["ludic.mypy_plugin"]
            """,
            language="toml",
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
                Link("Discord", to=config.DISCORD_INVITE_URL),
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
