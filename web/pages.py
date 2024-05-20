from typing import override

from ludic.attrs import GlobalAttrs
from ludic.catalog.layouts import Box, Center, Sidebar, Stack, WithSidebar
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.html import a, meta
from ludic.types import AnyChildren, Component
from ludic.web import Request

from .components import Footer, Menu


class BasePage(Component[AnyChildren, GlobalAttrs]):
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
                *self.children,
                htmx_version="1.9.10",
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
                Box(
                    Center(Stack(a("The Ludic Framework", href="/"))),
                    classes=["no-border", "no-inline-padding", "invert"],
                ),
                Box(
                    Center(
                        Stack(
                            WithSidebar(
                                Sidebar(Menu(**self.attrs_for(Menu))),
                                Stack(
                                    *self.children, Footer(), **self.attrs_for(Stack)
                                ),
                            ),
                            **self.attrs_for(Stack),
                        )
                    ),
                    classes=["no-inline-padding", "transparent"],
                ),
            ),
        )
