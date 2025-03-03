from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.messages import Message, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b
from ludic.web import Request

from web import config
from web.pages import Page


def integrations(request: Request) -> Page:
    return Page(
        H1("Other Integrations"),
        Paragraph(
            "This guide will walk you through the process of integrating the Ludic "
            "framework with other projects (aside from Starlette integration, which "
            f"is covered in the {
                Link('Web Framework', to=request.url_for('docs:web_framework').path)
            } section of the "
            "documentation). Here is the list of currently supported integrations:"
        ),
        List(
            Item(Link("FastAPI", to="#fastapi")),
            Item(Link("Django", to="#django")),
        ),
        H2("FastAPI", id="fastapi"),
        Paragraph(
            "This guide will walk you through integrating the Ludic framework with a "
            "FastAPI project. We will cover the necessary setup steps and provide "
            "examples of how to use Ludic in your FastAPI application."
        ),
        H3("Installation"),
        Paragraph("To install Ludic with FastAPI support, use the following command:"),
        CodeBlock('pip install "ludic[fastapi]"', language="sh"),
        H3("Setup"),
        Paragraph(
            f"Integrating Ludic with {Code('FastAPI')} is straightforward. Simply "
            f"configure the {Code('LudicRoute')} route class:"
        ),
        CodeBlock(
            """
            from fastapi import FastAPI
            from ludic.contrib.fastapi import LudicRoute

            app = FastAPI()
            app.router.route_class = LudicRoute
            """,
            language="python",
        ),
        H3("Creating Endpoints with Ludic"),
        Paragraph("You can return Ludic components directly from FastAPI endpoints:"),
        CodeBlock(
            """
            from fastapi import FastAPI
            from ludic.html import html, head, body, div, h1, p, title, b
            from ludic.contrib.fastapi import LudicRoute

            app = FastAPI()
            app.router.route_class = LudicRoute

            @app.get("/")
            def index() -> html:
                return html(
                    head(title("My Page")),
                    body(
                        div(
                            h1("My Homepage"),
                            p(f"Hello {b('World!')}"),
                            id="container",
                        )
                    )
                )
            """,
            language="python",
        ),
        H3("Using Predefined Components"),
        Paragraph("You can also use predefined components from Ludic's catalog:"),
        CodeBlock(
            """
            import json
            from fastapi import FastAPI, Request
            from ludic.catalog.pages import HtmlPage, Head, Body
            from ludic.catalog.headers import H1
            from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
            from ludic.catalog.layouts import Center, Stack
            from ludic.components import Component
            from ludic.types import AnyChildren
            from ludic.contrib.fastapi import LudicRoute

            app = FastAPI()
            app.router.route_class = LudicRoute

            class MyPage(Component[AnyChildren, GlobalAttrs]):
                def render(self) -> HtmlPage:
                    return HtmlPage(
                        Head(title="My Page"),
                        Body(
                            Center(
                                Stack(*self.children, **self.attrs),
                                style={"padding-block": "xxl"},
                            ),
                            htmx_version="2.0.0",
                        ),
                    )

            @app.get("/")
            async def index_with_components(request: Request) -> MyPage:
                query_params = dict(request.query_params)
                return MyPage(
                    H1("Demo Using The Catalog"),
                    Paragraph(
                        "This page is using components from "
                        f"{Link('Ludic framework.', to='https://getludic.dev')}"
                    ),
                    Paragraph(f"Here is the content of {Code('request.query_params')}"),
                    CodeBlock(json.dumps(query_params, indent=4), language="json"),
                )
            """,
            language="python",
        ),
        H3("Manual Response Handling"),
        Paragraph(f"If you need more control, use {Code('LudicResponse')} explicitly:"),
        CodeBlock(
            """
            from fastapi import FastAPI
            from ludic.html import p
            from ludic.contrib.fastapi import LudicResponse, LudicRoute

            app = FastAPI()
            app.router.route_class = LudicRoute

            @app.get("/custom")
            def custom_response() -> LudicResponse:
                return LudicResponse(
                    p("Hello, World!"),
                    status_code=201,
                    headers={"X-Custom-Header": "Ludic"}
                )
            """,
            language="python",
        ),
        H3("Example"),
        Paragraph("You can check a working FastAPI example:"),
        List(
            Item(
                Link(
                    "in the examples section",
                    to=request.url_path_for("examples:cascading_selects"),
                )
            ),
            Item(
                Link(
                    "source code on GitHub",
                    to=f"{config.GITHUB_REPO_URL}/blob/main/examples/fastapi_example.py",
                )
            ),
        ),
        H2("Django", id="django"),
        Paragraph(
            "This guide wil walk you through integration of the Ludic framework with "
            "a Django project. We will cover the necessary setup steps, how to "
            "configure middleware, and provide examples of how to use Ludic in your "
            "Django views."
        ),
        H3("Installation"),
        Paragraph("First, you need to install Ludic. You can do this using pip:"),
        CodeBlock('pip install "ludic[django]"'),
        H3("Middleware Configuration"),
        Paragraph(
            "To use Ludic with Django, you need to add the Ludic middleware to your "
            "Django settings. This middleware helps manage the Ludic elements during "
            "the request-response cycle, clean up cache, and so on.",
        ),
        NumberedList(
            Item(f"Open your {Code('settings.py')} file."),
            Item(f"Add {Code('LudicMiddleware')} to the {Code('MIDDLEWARE')} list:"),
        ),
        CodeBlock(
            """
            MIDDLEWARE = [
                # other middlewares...
                "ludic.contrib.django.LudicMiddleware",
            ]
            """,
            language="python",
        ),
        H3("Creating Views with Ludic"),
        Paragraph(
            "Let's create a simple HTML page using Ludic elements in a Django view. "
            f"Here is the content of the {Code('views.py')} file rendering a valid "
            "HTML page:"
        ),
        CodeBlock(
            """
            from django.http import HttpRequest
            from ludic.contrib.django import LudicResponse
            from ludic.html import html, head, body, div, h1, p, title, b


            def index(request: HttpRequest) -> LudicResponse:
                return LudicResponse(
                    html(
                        head(
                            title("My Page"),
                        ),
                        body(
                            div(
                                h1("My Homepage"),
                                p(f"Hello {b("World!")}"),
                                id="container",
                            )
                        )
                    )
                )
            """,
            language="python",
        ),
        Paragraph(
            f"However, you are not limited to {Code('ludic.html')} module. You can "
            f"build your own {
                Link('components', to=request.url_for('docs:components').path)
            } or use the ones available "
            f"in the {Link('catalog', to=request.url_for('catalog:index').path)}. "
            "Here is a simple example creating a page component and using it in a view:"
        ),
        CodeBlock(
            """
            import json

            from django.http import HttpRequest
            from ludic.attrs import GlobalAttrs
            from ludic.catalog.layouts import Center, Stack
            from ludic.catalog.pages import HtmlPage, Head, Body
            from ludic.catalog.headers import H1
            from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
            from ludic.components import Component
            from ludic.contrib.django import LudicResponse
            from ludic.types import AnyChildren


            class MyPage(Component[AnyChildren, GlobalAttrs]):
                def render(self) -> HtmlPage:
                    return HtmlPage(
                        Head(title="My Page"),
                        Body(
                            Center(
                                Stack(*self.children, **self.attrs),
                                style={"padding-block": self.theme.sizes.xxl},
                            ),
                            htmx_version="2.0.0",
                        ),
                    )


            def index_with_components(request: HttpRequest) -> LudicResponse:
                return LudicResponse(
                    MyPage(
                        H1("Demo Using The Catalog"),
                        Paragraph(
                            "This page is using components from "
                            f"{Link("Ludic framework.", to="https://getludic.dev")}"
                        ),
                        Paragraph(f"Here is the content of {Code("request.GET")}:"),
                        CodeBlock(
                            json.dumps(request.GET.dict(), indent=4),
                            language="json",
                        ),
                    )
                )
            """,
            language="python",
        ),
        Message(
            Title(b(f"Note about {Code('LudicResponse')}")),
            f"If you keep the {Code('LudicMiddleware')} in the {Code('MIDDLEWARE')} "
            "variable as the last, you can directly return Ludic components in your "
            f"views, without wrapping them in the {Code('LudicResponse')} class.",
        ),
        request=request,
        active_item="integrations",
        title="Ludic - Integrations",
    )
