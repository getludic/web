from typing import NotRequired, override

from ludic.attrs import Attrs, GlobalAttrs
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


class BasePageAttrs(Attrs):
    title: NotRequired[str]


class BasePage(Component[AnyChildren, BasePageAttrs]):
    @override
    def render(self) -> HtmlPage:
        return HtmlPage(
            Head(
                meta(charset="utf-8"),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                meta(
                    name="description",
                    content=(
                        "Lightweight framework for building dynamic HTML pages in "
                        "pure Python in minutes with a component approach similar to "
                        "React and without template engines."
                    ),
                ),
                meta(
                    name="keywords",
                    content=(
                        "ludic, framework, python, web development, htmx, html, "
                        "css, javascript, components"
                    ),
                ),
                meta(name="author", content="Pavel Dedik"),
                meta(name="robots", content="index, follow"),
                meta(
                    name="og:title",
                    content=self.attrs.get("title", "The Ludic Framework"),
                ),
                meta(
                    name="og:description",
                    content=(
                        "Lightweight framework for building dynamic HTML pages in "
                        "pure Python in minutes."
                    ),
                ),
                meta(name="og:url", content="https://getludic.dev"),
                meta(name="og:image", content="/static/logo.png"),
                meta(name="twitter:card", content="summary_large_image"),
                meta(
                    name="twitter:title",
                    content=self.attrs.get("title", "The Ludic Framework"),
                ),
                meta(
                    name="twitter:description",
                    content=(
                        "Lightweight framework for building dynamic HTML pages in "
                        "pure Python in minutes."
                    ),
                ),
                meta(name="twitter:image", content="/static/logo.png"),
                link(rel="icon", href="/static/favicon.png"),
                title=self.attrs.get("title", "The Ludic Framework"),
            ),
            Body(
                *self.children,
                htmx_version="1.9.12",
            ),
        )


class PageAttrs(Attrs):
    request: Request
    active_item: str
    title: NotRequired[str]


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
            title=self.attrs.get("title", "The Ludic Framework"),
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
