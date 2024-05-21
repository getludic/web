from typing import override

from ludic.attrs import Attrs, GlobalAttrs, NoAttrs
from ludic.catalog.buttons import ButtonLink
from ludic.catalog.layouts import (
    Box,
    Center,
    Cluster,
    Sidebar,
    Stack,
    Switcher,
    WithSidebar,
)
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.html import iframe, meta
from ludic.types import AnyChildren, Component
from ludic.web import Request

from .components import Footer, Menu, SearchBar


class BasePage(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> HtmlPage:
        return HtmlPage(
            Head(
                meta(charset="utf-8"),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                title="The Ludic Framework",
            ),
            Body(
                *self.children,
                htmx_version="1.9.12",
            ),
        )


class HeaderAttrs(Attrs):
    search_url: str


class Header(Component[AnyChildren, HeaderAttrs]):
    classes = ["header", "no-border", "no-inline-padding", "invert"]
    styles = {
        ".header .switcher > :nth-child(2)": {
            "flex-grow": "2",
        },
    }

    @override
    def render(self) -> Box:
        return Box(
            Center(
                Switcher(
                    Cluster(ButtonLink("Ludic Framework", to="/")),
                    Stack(
                        SearchBar(
                            hx_post=self.attrs["search_url"],
                            hx_trigger="input changed delay:500ms, search",
                            hx_target="#main-content",
                            hx_select="#main-content",
                        )
                    ),
                    Cluster(
                        iframe(
                            src=(
                                "https://ghbtns.com/github-btn.html"
                                "?user=paveldedik"
                                "&repo=ludic"
                                "&type=star"
                                "&count=true"
                                "&size=large"
                            ),
                            frameborder="0",
                            scrolling="0",
                            width=140,
                            height=30,
                            title="GitHub",
                        ),
                        classes=["flex-end"],
                    ),
                ),
            ),
        )


class PageAttrs(GlobalAttrs):
    request: Request
    active_item: str


class Page(Component[AnyChildren, PageAttrs]):
    @override
    def render(self) -> BasePage:
        return BasePage(
            Stack(
                Header(
                    search_url=self.attrs["request"].url_path_for("search_docs"),
                ),
                Box(
                    Center(
                        Stack(
                            WithSidebar(
                                Sidebar(Menu(**self.attrs_for(Menu))),
                                Stack(
                                    Stack(
                                        *self.children,
                                        id="main-content",
                                        **self.attrs_for(Stack),
                                    ),
                                    Footer(),
                                ),
                            ),
                            **self.attrs_for(Stack),
                        )
                    ),
                    classes=["no-inline-padding", "transparent"],
                ),
            ),
        )
