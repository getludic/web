from typing import override

from ludic.attrs import GlobalAttrs, NoAttrs
from ludic.catalog.layouts import (
    Box,
    Center,
    Cover,
    Sidebar,
    Stack,
    WithSidebar,
)
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.html import link, meta
from ludic.types import AnyChildren, Component
from ludic.web import Request

from .components import Footer, HomeHeader, MainHeader, Menu


class BasePage(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> HtmlPage:
        return HtmlPage(
            Head(
                meta(charset="utf-8"),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                link(rel="icon", href="/static/favicon.png"),
                title="The Ludic Framework",
            ),
            Body(
                *self.children,
                htmx_version="1.9.12",
            ),
        )


class PageAttrs(GlobalAttrs):
    request: Request
    active_item: str


class Page(Component[AnyChildren, PageAttrs]):
    @override
    def render(self) -> BasePage:
        return BasePage(
            Box(
                Center(
                    Stack(
                        MainHeader(
                            logo_url=self.attrs["request"]
                            .url_for("static", path="logo.png")
                            .path,
                            home_url=self.attrs["request"].url_for("index").path,
                            search_url=self.attrs["request"]
                            .url_for("search_docs")
                            .path,
                        ),
                        WithSidebar(
                            Sidebar(Menu(**self.attrs_for(Menu))),
                            Stack(
                                Stack(
                                    *self.children,
                                    id="main-content",
                                    **self.attrs_for(Stack),
                                ),
                            ),
                        ),
                        Footer(),
                        classes=["large"],
                    ),
                ),
                classes=["no-inline-padding", "transparent", "large"],
            ),
        )


class HomePageAttrs(GlobalAttrs):
    request: Request


class HomePage(Component[AnyChildren, HomePageAttrs]):
    @override
    def render(self) -> BasePage:
        return BasePage(
            Center(
                Cover(
                    HomeHeader(
                        home_url=self.attrs["request"].url_for("index").path,
                        logo_url=self.attrs["request"]
                        .url_for("static", path="logo.png")
                        .path,
                        docs_url=self.attrs["request"].url_for("docs:index").path,
                        catalog_url=self.attrs["request"].url_for("catalog:index").path,
                        examples_url=self.attrs["request"]
                        .url_for("examples:index")
                        .path,
                    ),
                    Stack(
                        *self.children,
                        classes=["cover-main", "text-align-center", "large"],
                    ),
                    Footer(),
                    classes=["no-inline-padding"],
                ),
            ),
        )
