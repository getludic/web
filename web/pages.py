import json
from typing import NotRequired, override

from ludic import Component
from ludic.attrs import Attrs
from ludic.catalog.layouts import Stack
from ludic.catalog.navigation import TableOfContents
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.html import aside, div, link, main, meta, script, style
from ludic.types import AnyChildren
from ludic.web import Request

from . import config
from .components import Menu, MobileMenu, PageActions, SiteFooter, SiteHeader
from .navigation import get_page, markdown_path
from .themes import dark_theme, light_theme

DESCRIPTION = (
    "Typed HTML components in pure Python. Ludic checks your markup with the "
    "type checker, mixes text and elements with t-strings and pairs with htmx."
)


def font_faces(request: Request) -> str:
    inter = request.url_for("static", path="fonts/inter-latin.woff2").path
    mono = request.url_for("static", path="fonts/jetbrains-mono-latin.woff2").path
    latin = (
        "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, "
        "U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, "
        "U+2212, U+2215, U+FEFF, U+FFFD"
    )
    return (
        "@font-face { font-family: Inter; font-style: normal; "
        "font-weight: 100 900; font-display: swap; "
        f'src: url("{inter}") format("woff2"); unicode-range: {latin}; }}\n'
        '@font-face { font-family: "JetBrains Mono"; font-style: normal; '
        "font-weight: 100 800; font-display: swap; "
        f'src: url("{mono}") format("woff2"); unicode-range: {latin}; }}'
    )


class BasePageAttrs(Attrs):
    request: Request
    title: NotRequired[str]
    active_section: NotRequired[str | None]
    markdown_url: NotRequired[str | None]


class BasePage(Component[AnyChildren, BasePageAttrs]):
    """The HTML document of every page: head, site header and footer."""

    styles = style.use(
        lambda theme: {
            ":root": {
                "scroll-padding-top": "5.5rem",
                "text-rendering": "optimizeLegibility",
            },
            ("section", "aside", "article", "details", "summary", "figure"): {
                "max-inline-size": "none",
            },
            ("h1", "h2", "h3", "h4"): {
                "color": theme.colors.dark.darken(1),
                "font-weight": "700",
                "letter-spacing": "-0.02em",
            },
            ("h1",): {
                "letter-spacing": "-0.035em",
                "line-height": 1.15,
            },
            ("h1 > span", "h2 > span", "h1 > .code", "h2 > .code", "h3 > .code"): {
                "line-height": 1.15,
            },
            ("pre", "code", "kbd", "samp"): {
                "font-variant-ligatures": "none",
            },
            ".with-anchor > a.anchor": {
                "opacity": "0",
                "transition": "opacity 0.15s",
            },
            (".with-anchor:hover > a.anchor", ".with-anchor > a.anchor:focus"): {
                "opacity": "1",
            },
            "::selection": {
                "background-color": theme.colors.primary.lighten(1),
            },
            ":focus-visible": {
                "outline": f"{theme.borders.normal} solid {theme.colors.primary}",
                "outline-offset": theme.borders.normal,
            },
            ("a.btn", "button.btn"): {
                "font-weight": "600",
                "line-height": 1.5,
                "padding": "0.45em 1em",
                "transition": "filter 0.15s, background-color 0.15s",
            },
            ("a.btn.small", "button.btn.small"): {
                "padding": "0.2em 0.65em",
                "font-size": theme.fonts.size * 0.875,
            },
            ("a.btn.large", "button.btn.large"): {
                "padding": "0.6em 1.3em",
                "font-size": theme.fonts.size * 1.05,
            },
            ("a.btn.primary", "button.btn.primary"): {
                "color": theme.colors.primary.readable(),
                "background-color": theme.colors.primary,
            },
            "@media (prefers-reduced-motion: reduce)": {
                "*, *::before, *::after": {
                    "animation-duration": "0.01ms !important",
                    "transition-duration": "0.01ms !important",
                },
            },
        }
    )

    @override
    def render(self) -> HtmlPage:
        request = self.attrs["request"]
        title = self.attrs.get("title", config.TITLE)
        image_url = str(request.url_for("static", path="ludic.png"))
        head_links = [
            link(
                rel="preload",
                href=request.url_for("static", path="fonts/inter-latin.woff2").path,
                as_="font",
                type="font/woff2",
                crossorigin=True,
            ),
            link(
                rel="icon",
                href=request.url_for("static", path="favicon.png").path,
                type="image/png",
            ),
        ]
        if markdown_url := self.attrs.get("markdown_url"):
            head_links.append(
                link(rel="alternate", type="text/markdown", href=markdown_url)
            )

        return HtmlPage(
            Head(
                meta(name="viewport", content="width=device-width, initial-scale=1"),
                meta(name="description", content=DESCRIPTION),
                meta(name="author", content=config.AUTHOR),
                meta(name="robots", content="index, follow"),
                meta(name="theme-color", content=light_theme.colors.white),
                meta(property="og:title", content=title),
                meta(property="og:description", content=DESCRIPTION),
                meta(property="og:url", content=config.HOME_URL),
                meta(property="og:image", content=image_url),
                meta(name="twitter:card", content="summary_large_image"),
                meta(name="twitter:title", content=title),
                meta(name="twitter:description", content=DESCRIPTION),
                meta(name="twitter:image", content=image_url),
                *head_links,
                style(font_faces(request)),
                script(
                    json.dumps(
                        {
                            "@context": "https://schema.org",
                            "@type": "SoftwareApplication",
                            "name": "Ludic",
                            "description": DESCRIPTION,
                            "applicationCategory": "DeveloperApplication",
                            "operatingSystem": "Cross-platform",
                            "programmingLanguage": "Python",
                            "url": config.HOME_URL,
                            "author": {"@type": "Person", "name": config.AUTHOR},
                            "sameAs": [config.GITHUB_REPO_URL],
                            "offers": {
                                "@type": "Offer",
                                "price": "0",
                                "priceCurrency": "USD",
                            },
                        }
                    ),
                    type="application/ld+json",
                ),
                title=title,
                theme=light_theme,
                dark_theme=dark_theme,
            ),
            Body(
                SiteHeader(
                    request=request,
                    active_section=self.attrs.get("active_section"),
                ),
                *self.children,
                SiteFooter(request=request),
                htmx_version=config.HTMX_VERSION,
            ),
        )


class PageAttrs(Attrs):
    request: Request
    active_item: str | None
    title: NotRequired[str]


class Page(Component[AnyChildren, PageAttrs]):
    """A page of the documentation, catalog or examples.

    The menu is on the left, the content in the middle, and the table of
    contents with links to edit the page and to its Markdown version on the
    right.
    """

    styles = style.use(
        lambda theme: {
            ".docs-layout": {
                "display": "grid",
                "grid-template-columns": "14rem minmax(0, 1fr) 13rem",
                "gap": theme.sizes.xxxl,
                "max-inline-size": "90rem",
                "margin-inline": "auto",
                "padding": f"{theme.sizes.xxl} {theme.sizes.l} 0",
            },
            (".docs-layout > .docs-sidebar", ".docs-layout > .docs-aside"): {
                "position": "sticky",
                "top": "5.5rem",
                "align-self": "flex-start",
                "max-block-size": "calc(100vh - 6.5rem)",
                "overflow-y": "auto",
            },
            ".docs-layout .docs-aside .table-of-contents": {
                "margin-block-end": theme.sizes.xl,
            },
            ".docs-layout > main": {
                "min-inline-size": "0",
                "max-inline-size": "50rem",
            },
            ".docs-layout #main-content > * + .with-anchor": {
                "margin-block-start": theme.sizes.xxxl,
            },
            ".docs-layout .page-footer": {
                "margin-block-start": theme.sizes.xxxl,
                "padding-block-start": theme.sizes.m,
                "border-block-start": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                ),
            },
            ".docs-layout .mobile-menu": {
                "display": "none",
                "margin-block-end": theme.sizes.l,
            },
            "@media (max-width: 75rem)": {
                ".docs-layout": {
                    "grid-template-columns": "13rem minmax(0, 1fr)",
                },
                ".docs-layout > .docs-aside": {
                    "display": "none",
                },
            },
            "@media (max-width: 52rem)": {
                ".docs-layout": {
                    "grid-template-columns": "minmax(0, 1fr)",
                    "padding-block-start": theme.sizes.l,
                },
                ".docs-layout > .docs-sidebar": {
                    "display": "none",
                },
                ".docs-layout .mobile-menu": {
                    "display": "block",
                },
            },
        }
    )

    @override
    def render(self) -> BasePage:
        request = self.attrs["request"]
        active_item = self.attrs["active_item"]

        markdown_url = None
        active_section = None
        if found := get_page(active_item):
            section, page = found
            active_section = section.name
            markdown_url = markdown_path(
                request.url_path_for(f"{section.name}:{page.name}")
            )

        actions = PageActions(request=request, markdown_url=markdown_url)
        return BasePage(
            div(
                aside(
                    Menu(request=request, active_item=active_item),
                    classes=["docs-sidebar"],
                ),
                main(
                    MobileMenu(request=request, active_item=active_item),
                    Stack(*self.children, id="main-content"),
                    div(actions, classes=["page-footer"]),
                ),
                aside(
                    TableOfContents(*self.children, label="On this page"),
                    actions,
                    classes=["docs-aside"],
                ),
                classes=["docs-layout"],
            ),
            request=request,
            title=self.attrs.get("title", config.TITLE),
            active_section=active_section,
            markdown_url=markdown_url,
        )


class HomePageAttrs(Attrs):
    request: Request


class HomePage(Component[AnyChildren, HomePageAttrs]):
    @override
    def render(self) -> BasePage:
        return BasePage(
            main(*self.children, id="main-content", classes=["home"]),
            request=self.attrs["request"],
            title=config.TITLE,
        )
