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

from . import config
from .components import EditOnGithub, Footer, HomeHeader, MainHeader, Menu


class BasePageAttrs(Attrs):
    title: NotRequired[str]
    request: Request


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
                    property="og:title",
                    content=self.attrs.get("title", config.TITLE),
                ),
                meta(
                    property="og:description",
                    content=(
                        "Lightweight framework for building dynamic HTML pages in "
                        "pure Python in minutes."
                    ),
                ),
                meta(property="og:url", content=config.HOME_URL),
                meta(
                    property="og:image",
                    content=self.attrs["request"].url_for("static", path="ludic.png"),
                ),
                meta(name="twitter:card", content="summary_large_image"),
                meta(
                    name="twitter:title",
                    content=self.attrs.get("title", config.TITLE),
                ),
                meta(
                    name="twitter:description",
                    content=(
                        "Lightweight framework for building dynamic HTML pages in "
                        "pure Python in minutes."
                    ),
                ),
                meta(
                    name="twitter:image",
                    content=self.attrs["request"].url_for("static", path="ludic.png"),
                ),
                link(
                    rel="icon",
                    href=self.attrs["request"]
                    .url_for("static", path="favicon.ico")
                    .path,
                ),
                title=self.attrs.get("title", config.TITLE),
            ),
            Body(
                *self.children,
                htmx_version=config.HTMX_VERSION,
            ),
        )


class PageAttrs(Attrs):
    request: Request
    active_item: str
    title: NotRequired[str]


class Page(Component[AnyChildren, PageAttrs]):
    @override
    def render(self) -> BasePage:
        request = self.attrs["request"]
        return BasePage(
            Box(
                Center(
                    Stack(
                        MainHeader(
                            logo_url=request.url_for("static", path="logo.png").path,
                            home_url=request.url_for("index").path,
                            search_url=request.url_for("search_docs").path,
                        ),
                        WithSidebar(
                            Sidebar(Menu(**self.attrs_for(Menu))),
                            Stack(
                                EditOnGithub(base_url=request.url.path),
                                *self.children,
                                id="main-content",
                                **self.attrs_for(Stack),
                            ),
                        ),
                        Footer(),
                        classes=["large"],
                    ),
                ),
                classes=["no-inline-padding", "transparent", "large"],
            ),
            title=self.attrs.get("title", config.TITLE),
            request=self.attrs["request"],
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
            request=self.attrs["request"],
        )
