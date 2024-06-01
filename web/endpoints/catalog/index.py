from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.lists import Item, List
from ludic.catalog.messages import (
    Message,
    Title,
)
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, i
from ludic.web import Request

from web.pages import Page


def index(request: Request) -> Page:
    return Page(
        H1("Catalog"),
        Paragraph(
            f"The {Code("ludic.catalog")} module is a collection of components "
            "designed to help build applications using the Ludic framework. It "
            "serves as both a resource for building new web applications and also "
            "as a showcase of ways to implement components."
        ),
        Paragraph(
            "Each item in the catalog is a reusable component that generates HTML "
            "code and registers its own CSS styles.. The registered CSS are loaded "
            f"using the {Code("style.load()")} method, as detailed in the "
            f"{Link("Styles and Themes", to=request.url_path_for("docs:styles"))} "
            "section of the documentation."
        ),
        Paragraph(
            f"The catalog components are like {b("Lego pieces")} you can assemble "
            f"together to build interactive and beautiful {b("HTML documents")} "
            f"with {b("minimalistic")} approach:"
        ),
        List(
            Item(
                "You write HTML in pure Python, this removes any need for template "
                "engines and offers type safety as a bonus."
            ),
            Item(
                "The generated CSS is simple, extensible, and easy to understand. "
                "The layouts you can use for building your pages are responsive, "
                "reusable, and robust. They are based on the amazing "
                f"{Link("Every Layout Book", to="https://every-layout.dev/")}."
            ),
        ),
        H2("How Do You Use The Catalog?"),
        Paragraph(
            f"In order for everything to work correctly, the first thing you usually "
            f"need to do is to create a {Code("Page")} component. This component is "
            "important for two reasons:"
        ),
        List(
            Item(
                "It renders as a valid HTML document with (optionally) HTMX script "
                "loaded;"
            ),
            Item(
                "It renders collected CSS styles loaded from components in the catalog."
            ),
        ),
        Message(
            Title("How does CSS loading work?"),
            f"The CSS styles for components are loaded when the component is imported "
            f"anywhere in your application. The {Code("style.load()")} method iterates "
            "over all imported components and checks if the components have any styles "
            "defined.",
        ),
        Paragraph(
            "All rendered HTML documents will have this component as a base similar to "
            f"how all HTML pages in template engines like Jinja2 use the {i("base")} "
            "template."
        ),
        Message(
            Title(
                f"How does a {Code("Page")} component differ from a regular component?"
            ),
            "The only difference is that it renders as a valid HTML5 document starting "
            f"with the {Code("<!doctype html>")} declaration. You usually need only "
            f"one {Code("Page")} component in the whole application.",
        ),
        Paragraph(
            f"After you are done with setting up your {Code("Page")} component, you "
            "can use it along with all the other components in the catalog."
        ),
        H3("HtmlPage Component"),
        Paragraph(
            "This component has already been mentioned throughout the documentation "
            f"and can be used to create your {Code("Page")} component. The "
            f"{Code("HtmlPage")} component is just for convenience so that you can "
            "quickly start and not worry about how to load e.g. CSS styles or HTMX. "
        ),
        Paragraph(
            f"Here is how you would use the {Code("HtmlPage")} component to "
            f"create your own {Code("Page")} component:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import NoAttrs
            from ludic.html import link, meta
            from ludic.catalog.pages import HtmlPage, Head, Body
            from ludic.catalog.layouts import Stack
            from ludic.types import AnyChildren, Component

            class Page(Component[AnyChildren, NoAttrs]):
                @override
                def render(self) -> HtmlPage:
                    return HtmlPage(
                        Head(
                            # add custom head elements
                            meta(charset="utf-8"),
                            link(rel="icon", type="image/png", href="..."),

                            # here is a list of the Head's (optional) attributes
                            title="My Page",        # add custom title
                            favicon="favicon.ico",  # add favicon path
                            load_styles=True,       # load registered styles
                            htmx_config=...,        # configure HTMX
                        ),
                        Body(
                            # here you can create a base layout where all children of
                            # this Page component will be placed, more about layouts
                            # in the layouts section
                            Stack(*self.children),

                            # here is a list of the Body's (optional) attributes
                            htmx_version="1.9.10",  # loads HTMX script from CDN
                            htmx_path="htmx.js",    # loads HTMX script from a path
                            htmx_enabled=True,      # enable HTMX
                        ),
                    )
            """,
            language="python",
        ),
        Paragraph("Here are the default values:"),
        List(
            Item(Code("load_styles=True")),
            Item(Code('htmx_config={"defaultSwapStyle": "outerHTML"}')),
            Item(Code("htmx_enabled=True")),
            Item(Code('htmx_version="latest"')),
        ),
        Paragraph(
            f"Now that you prepared your {Code("Page")} component, you can use it in "
            "your code like here:"
        ),
        CodeBlock(
            """
            from ludic.web import LudicApp
            from ludic.catalog.buttons import Button
            from ludic.catalog.headers import H1
            from ludic.catalog.typography import Paragraph

            from your_app.pages import Page

            app = LudicApp()

            @app.get("/")
            def index(request: Request) -> Page:
                return Page(
                    H1("Hello, World!"),
                    Button("Click Me", hx_get=request.url_for("clicked")),
                )

            @app.get("/clicked")
            def clicked(request: Request) -> Paragraph:
                return Paragraph("You clicked me!")
            """,
            language="python",
        ),
        Paragraph(
            f"The {Code("HtmlPage")} component comes also with default "
            f"{Code("styles")}. In fact, the following list of styles are "
            f"auto-loaded whenever you import anything from the {Code("ludic.catalog")}"
            " module:"
        ),
        List(
            Item(Code("ludic.catalog.pages")),
            Item(Code("ludic.catalog.layouts")),
        ),
        request=request,
        active_item="catalog:index",
        title="Ludic - The Catalog",
    )
