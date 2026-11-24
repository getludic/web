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
            t"The {Code('ludic.catalog')} module is a collection of components "
            t"designed to help build applications using the Ludic framework. It "
            t"serves as both a resource for building new web applications and also "
            t"as a showcase of ways to implement components."
        ),
        Paragraph(
            t"Each item in the catalog is a reusable component that generates HTML "
            t"code and registers its own CSS styles.. The registered CSS are loaded "
            t"using the {Code('style.load()')} method, as detailed in the "
            t"{Link('Styles and Themes', to=request.url_path_for('docs:styles'))} "
            t"section of the documentation."
        ),
        Paragraph(
            t"The catalog components are like {b('Lego pieces')} you can assemble "
            t"together to build interactive and beautiful {b('HTML documents')} "
            t"with {b('minimalistic')} approach:"
        ),
        List(
            Item(
                "You write HTML in pure Python, this removes any need for template "
                "engines and offers type safety as a bonus."
            ),
            Item(
                t"The generated CSS is simple, extensible, and easy to understand. "
                t"The layouts you can use for building your pages are responsive, "
                t"reusable, and robust. They are based on the amazing "
                t"{Link('Every Layout Book', to='https://every-layout.dev/')}."
            ),
        ),
        H2("How Do You Use The Catalog?"),
        Paragraph(
            t"In order for everything to work correctly, the first thing you usually "
            t"need to do is to create a {Code('Page')} component. This component is "
            t"important for two reasons:"
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
            t"The CSS styles for components are loaded when the component is imported "
            t"anywhere in your application. The {Code('style.load()')} method iterates "
            t"over all imported components and checks if the components have any "
            t"styles defined.",
        ),
        Paragraph(
            t"All rendered HTML documents will have this component as a base "
            t"similar to how all HTML pages in template engines like Jinja2 use the "
            t"{i('base')} template."
        ),
        Message(
            Title(
                t"How does a {Code('Page')} component differ from a regular component?"
            ),
            t"The only difference is that it renders as a valid HTML5 document "
            t"starting with the {Code('<!doctype html>')} declaration. You usually "
            t"need only one {Code('Page')} component in the whole application.",
        ),
        Paragraph(
            t"After you are done with setting up your {Code('Page')} component, you "
            t"can use it along with all the other components in the catalog."
        ),
        H3("HtmlPage Component"),
        Paragraph(
            t"This component has already been mentioned throughout the documentation "
            t"and can be used to create your {Code('Page')} component. The "
            t"{Code('HtmlPage')} component is just for convenience so that you can "
            t"quickly start and not worry about how to load e.g. CSS styles or HTMX. "
        ),
        Paragraph(
            t"Here is how you would use the {Code('HtmlPage')} component to "
            t"create your own {Code('Page')} component:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import NoAttrs
            from ludic.html import link, meta
            from ludic.catalog.pages import HtmlPage, Head, Body
            from ludic.catalog.layouts import Stack
            from ludic.components import Component
            from ludic.types import AnyChildren

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
                            htmx_version="2.0.11",  # loads HTMX script from CDN
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
            t"Now that you prepared your {Code('Page')} component, you can use it in "
            t"your code like here:"
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
            t"The {Code('HtmlPage')} component comes also with default "
            t"{Code('styles')}. In fact, the following list of styles are "
            t"auto-loaded whenever you import anything from the {Code('ludic.catalog')}"
            t" module:"
        ),
        List(
            Item(Code("ludic.catalog.pages")),
            Item(Code("ludic.catalog.layouts")),
        ),
        request=request,
        active_item="catalog:index",
        title="Ludic - The Catalog",
    )
