from ludic.catalog.buttons import Button
from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.layouts import Box, Cluster, Stack
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.messages import Message, MessageWarning, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b
from ludic.web import LudicApp, Request

from web.pages import PageWithMenu

app = LudicApp()


@app.get(path="/htmx/")
def htmx(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Using HTMX with Ludic"),
        Paragraph(
            f"{Link('HTMX', to='https://htmx.org')} is a powerful library that "
            "simplifies the creation of dynamic, interactive web pages. It lets you "
            "achieve the responsiveness of single-page applications without the "
            "complexity of writing extensive JavaScript code. HTMX works by extending "
            "standard HTML with special attributes that control how elements interact "
            "with the server."
        ),
        Paragraph(
            "The most typical example is when you want to fetch content from a server "
            "on a button click event and append or replace content on your page with "
            f"the response. You can examine a similar example {Link(
                "bellow", to="#sample-swap-operation")}."
        ),
        Paragraph(
            "Here is a couple of HTMX attributes that allow you to add dynamic ",
            "functionality to your pages:",
        ),
        List(
            Item(Code("hx-get"), " – issues a GET request to the server"),
            Item(Code("hx-post"), " – issues a POST request to the server"),
            Item(
                Code("hx-target"),
                " – specifies which element is replaced by the response",
            ),
            Item(
                Code("hx-select "),
                " – specifies which element from the response is replaces",
            ),
            Item(Code("hx-swap"), " – controls how content is swapped"),
            Item(Code("hx-trigger"), " – specifies which event triggers the request"),
        ),
        Message(
            Title("HTMX Attributes Reference"),
            f"Check all the available attributes in the {Link(
                "HTMX documentation", to="https://htmx.org/reference/")}.",
        ),
        H2("HTMX Integration in Ludic"),
        Paragraph(
            f"The {Code("ludic.html")} module seamlessly supports HTMX attributes, "
            "making it easy to add dynamic functionality to your pages. Let's see "
            "a simple example:"
        ),
        CodeBlock(
            """
            from ludic.html import button

            button("Click Me", hx_post="/clicked", hx_swap="innerHTML")
            """,
            language="python",
        ),
        Paragraph("This code would generate the following HTML:"),
        CodeBlock(
            """
            <button hx-post="/clicked" hx-swap="innerHTML">
                Click Me
            </button>
            """,
            language="html",
        ),
        H2("Setting up an HTMX-Enabled Page"),
        NumberedList(
            Item(
                f"{b("Include the HTMX library")}: Add the HTMX script to your base "
                "HTML component",
                CodeBlock(
                    """
                    from typing import override

                    from ludic.catalog.pages import HtmlPage, Head, Body
                    from ludic.types import AnyChildren, Component, NoAttrs


                    class Page(Component[AnyChildren, NoAttrs]):
                        @override
                        def render(self) -> HtmlPage:
                            return HtmlPage(
                                Head(title="My App"),
                                Body(*self.children, htmx_version="1.9.10"),
                            )
                    """,
                    language="python",
                ),
            ),
            Item(
                f"{b(f"Use the {Code("Page")} component")}: Employ the Page component "
                "as the foundation for your HTML documents to ensure they load the "
                "necessary HTMX script."
            ),
        ),
        MessageWarning(
            Title(f"Default {Code("hx-swap")} Operation"),
            f"The default HTMX swap operation is set to {Code("outerHTML")} in all "
            f"pages based on the {Code("HtmlPage")} component. This is different "
            f"than HTMX default which is {Code("innerHTML")}.",
        ),
        H2("Sample Swap Operation"),
        Paragraph("Let's illustrate how to create a dynamic page with HTMX and Ludic:"),
        CodeBlock(
            """
            from ludic.html import b, div, p, button
            from ludic.web import LudicApp, Request

            from your_app.pages import Page

            app = LudicApp()

            @app.get("/")
            def homepage(request: Request) -> Page:
                return Page(
                    p(
                        "This is a simple example with one button performing the "
                        "hx-swap operation."
                    ),
                    button("Show Hidden Content", hx_get=request.url_for(content)),
                )

            @app.get("/content")
            def content() -> p:
                return p(b("This is the hidden content."))
            """,
            language="python",
        ),
        Paragraph("You can test the performed action here:"),
        Box(htmx_example(request)),
        H3("Explanation"),
        List(
            Item(
                f"{b("Button Behavior")}: Clicking the button triggers an HTTP GET "
                f"request to {Code("/content")}. The response replaces the original "
                f"button with the content returned from the {Code("/content")} "
                "endpoint."
            ),
            Item(
                f"{b("Web Framework")}: Ludic acts as a web framework (built on "
                f"{Link("Starlette", to="https://www.starlette.io/")}), empowering you "
                f"to define endpoints and handle requests. Explore the {Link(
                    "Web Framework", to=request.url_for("web_framework").path)} "
                "section of the documentation for in-depth information."
            ),
        ),
        H2("Headers"),
        Paragraph(
            "It is possible to append custom HTMX headers in responses, here is an "
            "example:"
        ),
        CodeBlock(
            """
            from ludic import types
            from ludic.html import p

            from your_app.server import app

            @app.get("/")
            def index() -> tuple[p, types.HXHeaders]:
                return p("Example"), {"HX-Location": {"path": "/", "target": "#test"}}
            """,
            language="python",
        ),
        Paragraph(
            f"You can also change the return type of your endpoint with {Code(
                "tuple[div, types.Headers]")} which allows arbitrary headers, not just "
            "HTMX-specific ones."
        ),
        H2("Rendering JavaScript"),
        Paragraph(
            "In some cases, HTMX components require some JavaScript code. For that "
            f"purpose, there is the {Code("ludic.types.JavaScript")} class:"
        ),
        CodeBlock(
            """
            from ludic.html import button, div, h2, table
            from ludic.types import JavaScript

            from your_app.server import app

            @app.get("/data")
            def data() -> div:
                return div(
                    h2("Data"),
                    table(...),
                    button("Click Here", onclick=JavaScript("alert('test')")),
                )
            """,
            language="python",
        ),
        request=request,
        active_item="htmx",
    )


@app.get("/htmx/example/")
def htmx_example(request: Request) -> Stack:
    return Stack(
        Paragraph(
            "This is a simple example with one button performing the "
            f"{Code("hx-swap")} operation."
        ),
        Cluster(
            Button("Show Hidden Content", hx_get=request.url_for(htmx_content)),
            classes=["centered"],
        ),
    )


@app.get("/htmx/content/")
def htmx_content() -> Paragraph:
    return Paragraph(b("This is the hidden content."))
