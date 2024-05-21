from typing import override

from ludic.attrs import Attrs, GlobalAttrs, NoAttrs
from ludic.base import AnyChildren
from ludic.catalog.buttons import ButtonLink
from ludic.catalog.forms import InputField
from ludic.catalog.layouts import Box, Cluster, Stack
from ludic.catalog.navigation import NavHeader, Navigation, NavItem, NavSection
from ludic.catalog.typography import Link
from ludic.html import div, img, style
from ludic.types import Component, NoChildren
from ludic.web import Request


class HeaderAttrs(Attrs):
    logo_url: str


class Header(Component[NoChildren, HeaderAttrs]):
    @override
    def render(self) -> div:
        return div(
            img(
                src=self.attrs["logo_url"],
                alt="Ludic Logo",
                style={"max-width": "60ch"},
            ),
            classes=["text-align-center"],
        )


class Div(div):
    classes = ["showcase"]
    styles = style.use(
        lambda theme: {
            ".showcase": {
                "color": theme.colors.light.darken(2),
                "background-color": theme.colors.light.darken(2),
                "padding-block": theme.sizes.xs,
            },
        }
    )


class MenuAttrs(Attrs):
    request: Request
    active_item: str


class Menu(Component[NoChildren, MenuAttrs]):
    @override
    def render(self) -> Box:
        request = self.attrs["request"]
        return Box(
            Navigation(
                NavItem(
                    "Introduction",
                    to=request.url_for("index"),
                    active=self.attrs["active_item"] == "index",
                ),
                NavSection(
                    NavHeader("Framework"),
                    NavItem(
                        "Getting Started",
                        to=request.url_for("getting_started"),
                        active=self.attrs["active_item"] == "getting_started",
                    ),
                    NavItem(
                        "Components",
                        to=request.url_for("components"),
                        active=self.attrs["active_item"] == "components",
                    ),
                    NavItem(
                        "Styles and Themes",
                        to=request.url_for("styles"),
                        active=self.attrs["active_item"] == "styles",
                    ),
                    NavItem(
                        "HTMX Support",
                        to=request.url_for("htmx"),
                        active=self.attrs["active_item"] == "htmx",
                    ),
                    NavItem(
                        "Web Framework",
                        to=request.url_for("web_framework"),
                        active=self.attrs["active_item"] == "web_framework",
                    ),
                ),
                NavSection(
                    NavHeader("Catalog"),
                    NavItem(
                        "Basics",
                        to=request.url_for("catalog"),
                        active=self.attrs["active_item"] == "catalog",
                    ),
                    NavItem(
                        "Layouts",
                        to=request.url_for("layouts"),
                        active=self.attrs["active_item"] == "layouts",
                    ),
                    NavItem(
                        "Typography",
                        to=request.url_for("typography"),
                        active=self.attrs["active_item"] == "typography",
                    ),
                    NavItem(
                        "Buttons",
                        to=request.url_for("buttons"),
                        active=self.attrs["active_item"] == "buttons",
                    ),
                    NavItem(
                        "Messages",
                        to=request.url_for("messages"),
                        active=self.attrs["active_item"] == "messages",
                    ),
                    NavItem(
                        "Loaders",
                        to=request.url_for("loaders"),
                        active=self.attrs["active_item"] == "loaders",
                    ),
                    NavItem(
                        "Tables",
                        to=request.url_for("tables"),
                        active=self.attrs["active_item"] == "tables",
                    ),
                    NavItem(
                        "Forms",
                        to=request.url_for("forms"),
                        active=self.attrs["active_item"] == "forms",
                    ),
                ),
                NavSection(
                    NavHeader("Examples"),
                    NavItem(
                        "Bulk Update",
                        to=request.url_for("bulk_update"),
                        active=self.attrs["active_item"] == "bulk-update",
                    ),
                    NavItem(
                        "Click To Edit",
                        to=request.url_for("click_to_edit"),
                        active=self.attrs["active_item"] == "click-to-edit",
                    ),
                    NavItem(
                        "Click To Load",
                        to=request.url_for("click_to_load"),
                        active=self.attrs["active_item"] == "click-to-load",
                    ),
                    NavItem(
                        "Delete Row",
                        to=request.url_for("delete_row"),
                        active=self.attrs["active_item"] == "delete-row",
                    ),
                    NavItem(
                        "Edit Row",
                        to=request.url_for("edit_row"),
                        active=self.attrs["active_item"] == "edit-row",
                    ),
                    NavItem(
                        "Infinite Scroll",
                        to=request.url_for("infinite_scroll"),
                        active=self.attrs["active_item"] == "infinite-scroll",
                    ),
                    NavItem(
                        "Lazy Loading",
                        to=request.url_for("lazy_loading"),
                        active=self.attrs["active_item"] == "lazy-loading",
                    ),
                ),
                hx_boost=True,
            ),
        )


class Footer(Component[NoChildren, NoAttrs]):
    @override
    def render(self) -> Box:
        return Box(
            (
                f"Made with {Link("Ludic", to="https://github.com/paveldedik/ludic")} "
                f"and {Link("HTMX", to="https://htmx.org")}"
            ),
            classes=[
                "no-inline-padding",
                "transparent",
                "text-align-center",
            ],
            style={
                "margin-block-start": self.theme.sizes.xxxxl,
                "margin-block-end": self.theme.sizes.l,
            },
        )


class SearchBar(Component[NoChildren, GlobalAttrs]):
    classes = ["search-bar"]
    styles = style.use(
        lambda theme: {
            ".search-bar": {
                'input[type="search"]': {
                    "background-color": theme.colors.dark.lighten(1),
                    "border": f"1px solid {theme.colors.dark.lighten(5)}",
                    "border-radius": theme.rounding.less,
                    "font-size": theme.fonts.size * 0.9,
                    "color": "#fff",
                    "transition": "all 0.3s ease-in-out",
                },
                'input[type="search"]::placeholder': {
                    "color": theme.colors.light.darken(8),
                },
                'input[type="search"]:focus': {
                    "border-color": theme.colors.light.darken(5),
                    "outline": "none",
                },
                'input[type="search"]::-webkit-search-cancel-button': {
                    "-webkit-appearance": "none",  # type: ignore
                },
            },
        }
    )

    @override
    def render(self) -> InputField:
        return InputField(
            type="search",
            name="search",
            label=None,
            placeholder="Search in the docs ...",
            **self.attrs,
        )


class SearchResultAttrs(Attrs):
    title: AnyChildren
    content: AnyChildren
    url: str


class SearchResult(Component[NoChildren, SearchResultAttrs]):
    classes = ["search-result"]
    styles = {
        ".search-result": {
            "font-style": "italic",
        },
        ".search-result a.btn": {
            "font-style": "normal",
        },
        ".search-result .anchor": {
            "display": "none",
        },
    }

    @override
    def render(self) -> Box:
        return Box(
            Stack(
                self.attrs["title"],
                self.attrs["content"],
                Cluster(
                    ButtonLink(
                        "Read More",
                        to=self.attrs["url"],
                        classes=["large", "secondary"],
                    ),
                    classes=["centered"],
                ),
            ),
        )
