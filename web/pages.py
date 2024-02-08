from typing import override

from ludic.attrs import Attrs, GlobalAttrs
from ludic.catalog.layouts import Box, Center, Sidebar, Stack, WithSidebar
from ludic.catalog.navigation import NavHeader, Navigation, NavItem, NavSection
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.catalog.typography import Link
from ludic.html import a, meta
from ludic.types import AnyChildren, Component, NoAttrs, NoChildren
from ludic.web import Request


class Page(Component[AnyChildren, GlobalAttrs]):
    @override
    def render(self) -> HtmlPage:
        self.attrs.setdefault("id", "content")
        return HtmlPage(
            Head(
                meta(charset="utf-8"),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                title="The Ludic Framework",
            ),
            Body(
                Stack(
                    Box(
                        Center(Stack(a("The Ludic Framework", href="/"))),
                        classes=["no-border", "no-inline-padding", "invert"],
                    ),
                    Box(
                        Center(Stack(*self.children, **self.attrs_for(Stack))),
                        classes=["no-inline-padding", "transparent"],
                    ),
                ),
                htmx_version="1.9.10",
            ),
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
                        "Tables",
                        to=request.url_for("tables"),
                        active=self.attrs["active_item"] == "tables",
                    ),
                    NavItem(
                        "Forms",
                        to=request.url_for("forms"),
                        active=self.attrs["active_item"] == "forms",
                    ),
                    NavItem(
                        "Layouts",
                        to=request.url_for("layouts"),
                        active=self.attrs["active_item"] == "layouts",
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
                f"and {Link('HTMX', to='https://htmx.org')}"
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


class PageWithMenuAttrs(GlobalAttrs):
    request: Request
    active_item: str


class PageWithMenu(Component[AnyChildren, PageWithMenuAttrs]):
    @override
    def render(self) -> Page:
        return Page(
            WithSidebar(
                Sidebar(Menu(**self.attrs_for(Menu))),
                Stack(*self.children, Footer(), **self.attrs_for(Stack)),
            ),
        )
