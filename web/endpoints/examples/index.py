from typing import override

from ludic import Component
from ludic.attrs import GlobalAttrs, NoAttrs
from ludic.catalog.buttons import ButtonLink
from ludic.catalog.forms import InputField
from ludic.catalog.headers import H1, H2
from ludic.catalog.layouts import Box, Cluster
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import style
from ludic.types import NoChildren
from ludic.web import Request

from web.pages import Page


class SampleHeader(Component[NoChildren, NoAttrs]):
    classes = ["sample-navigation"]

    @override
    def render(self) -> Box:
        return Box(
            Cluster(
                ButtonLink("Logo", to="#"),
                Cluster(
                    ButtonLink("Item 1", to="#"),
                    ButtonLink("Item 2", to="#"),
                    ButtonLink("Item 3", to="#"),
                    ButtonLink("Item 4", to="#", classes=["success"]),
                ),
                classes=["justify-space-between"],
            ),
            classes=["invert"],
        )


class SampleSearch(Component[NoChildren, GlobalAttrs]):
    classes = ["search-bar-sample"]
    styles = style.use(
        lambda theme: {
            ".search-bar-sample": {
                "input": {
                    "background-color": theme.colors.light.lighten(1),
                    "border": f"1px solid {theme.colors.light.darken(5)}",
                    "color": theme.colors.dark,
                },
                "input::placeholder": {
                    "color": theme.colors.dark.lighten(7),
                },
                "input:focus": {
                    "border-color": theme.colors.dark.lighten(5),
                    "outline": "none",
                },
            },
        }
    )

    @override
    def render(self) -> InputField:
        return InputField(
            type="search",
            label=None,
            placeholder="Custom search bar",
            **self.attrs,
        )


async def index(request: Request) -> Page:
    return Page(
        H1("Components and Styling"),
        Paragraph(
            "Here is a couple of examples how to write Ludic components, how to add "
            "custom HTML classes and register CSS properties."
        ),
        H2("Link"),
        Paragraph(
            "A simple component simulating a link. The component only accepts one "
            f"string child and a {Code('to')} attribute."
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import Attrs
            from ludic.components import Component
            from ludic.html import a

            class LinkAttrs(Attrs):
                to: str

            class Link(Component[str, LinkAttrs]):
                classes = ["link"]

                @override
                def render(self) -> a:
                    return a(
                        *self.children,
                        href=self.attrs["to"],
                        style={"color": self.theme.colors.warning},
                    )
            """,
            language="python",
        ),
        H2("Navigation"),
        Paragraph(
            "A simple component which renders a navigation bar with a logo and "
            "a couple of links aligned to the right. This is what it looks like:"
        ),
        SampleHeader(),
        Paragraph("And here is the code for this example:"),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import NoAttrs
            from ludic.catalog.buttons import ButtonLink
            from ludic.catalog.layouts import Box, Cluster
            from ludic.components import Component
            from ludic.types import NoChildren

            class Navigation(Component[NoChildren, NoAttrs]):
                classes = ["sample-navigation"]

                @override
                def render(self) -> Box:
                    return Box(
                        Cluster(
                            ButtonLink("Logo"),
                            Cluster(
                                ButtonLink("Item 1", to="..."),
                                ButtonLink("Item 2", to="..."),
                                ButtonLink("Item 3", to="..."),
                                ButtonLink("Item 4", to="...", classes=["success"]),
                            ),
                            classes=["justify-space-between"],
                        ),
                        classes=["invert"],
                    )
            """,
            language="python",
        ),
        Paragraph(
            "Note that you need to use this navigation in the context of the "
            f"{
                Link(
                    'HtmlPage',
                    to=f'{request.url_path_for("catalog:index")}#htmlpage-component',
                )
            } "
            "component, otherwise there won't be the necessary CSS loaded. Or you can "
            "define your own styles for the component."
        ),
        H2("Search Bar"),
        Paragraph(
            "A simple component rendering a search bar with custom styling. Here is "
            "what it looks like:"
        ),
        SampleSearch(),
        Paragraph("And here is the code for this example:"),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import GlobalAttrs
            from ludic.catalog.forms import InputField
            from ludic.html import style
            from ludic.components import Component
            from ludic.types import NoChildren

            class SearchBar(Component[NoChildren, GlobalAttrs]):
                classes = ["search-bar"]
                styles = style.use(
                    lambda theme: {
                        ".search-bar": {
                            "input": {
                                "background-color": theme.colors.light.lighten(1),
                                "border": f"1px solid {theme.colors.light.darken(5)}",
                                "color": theme.colors.dark,
                            },
                            "input::placeholder": {
                                "color": theme.colors.dark.lighten(7),
                            },
                            "input:focus": {
                                "border-color": theme.colors.dark.lighten(5),
                                "outline": "none",
                            },
                        },
                    }
                )

                @override
                def render(self) -> InputField:
                    return InputField(
                        type="search",
                        placeholder="Custom search bar",
                        **self.attrs,
                    )
            """,
            language="python",
        ),
        request=request,
        active_item="examples:index",
        title="Ludic - Examples",
    )
