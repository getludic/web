from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.messages import Message, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b
from ludic.web import Request

from web.pages import Page


def integrations(request: Request) -> Page:
    return Page(
        H1("Integrations"),
        Paragraph(
            "This guide will walk you through the process of integrating the Ludic "
            "framework with other projects. Here is the list of currently supported "
            "integrations:"
        ),
        List(
            Item(Link("Django", to="#django")),
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
        H3("Creating Views with Ludic"),
        Paragraph(
            "Let's create a simple HTML page using Ludic in a Django view. "
            f"Here is the content of the {Code("views.py")} file:"
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
            f"However, you are not limited to {Code("ludic.html")} module. You can "
            f"build {Link("components", to=request.url_for("docs:components").path)} "
            f"or use the ones available in the {Link("catalog",
                to=request.url_for("catalog:index").path)}. Here is a simple view "
            "using a page component:"
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
        H3("Middleware Configuration"),
        Paragraph(
            "To use Ludic with Django, you need to add the Ludic middleware to your "
            "Django settings. This middleware helps manage the Ludic elements during "
            "the request-response cycle, clean up cache, and so on.",
        ),
        NumberedList(
            Item(f"Open your {Code("settings.py")} file."),
            Item(f"Add {Code("LudicMiddleware")} to the {Code("MIDDLEWARE")} list:"),
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
        Message(
            Title(b("Note about views")),
            "If you keep the middleware in the last position, you can directly "
            "return Ludic elements or components in your views, without wrapping "
            f"them in the {Code("LudicResponse")} class.",
        ),
        request=request,
        active_item="integrations",
        title="Ludic - Integrations",
    )
