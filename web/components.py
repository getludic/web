from typing import override

from ludic import Component
from ludic.attrs import Attrs, GlobalAttrs
from ludic.catalog.cards import Card
from ludic.catalog.forms import InputField
from ludic.catalog.layouts import Cluster
from ludic.catalog.navigation import NavBar, Navigation, NavItem
from ludic.catalog.pages import ColorSchemeToggle
from ludic.components import Block
from ludic.html import (
    a,
    b,
    blockquote,
    details,
    div,
    footer,
    img,
    li,
    nav,
    p,
    span,
    style,
    summary,
    ul,
)
from ludic.types import AnyChildren, NoChildren, Safe
from ludic.web import Request

from . import config
from .navigation import SECTIONS, get_page

GITHUB_ICON = Safe(
    '<svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor" '
    'aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 '
    "7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09"
    "-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 "
    "1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59"
    ".82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 "
    "0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27"
    ".82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 "
    '2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
)


class BadgeAttrs(Attrs):
    url: str
    img_url: str
    title: str


class Badge(Component[NoChildren, BadgeAttrs]):
    @override
    def render(self) -> a:
        return a(
            img(src=self.attrs["img_url"], alt=self.attrs["title"]),
            href=self.attrs["url"],
            title=self.attrs["title"],
        )


class LogoAttrs(Attrs):
    home_url: str
    logo_url: str


class Logo(Component[NoChildren, LogoAttrs]):
    """The Ludic logo, with its colors inverted in the dark theme."""

    classes = ["logo"]
    styles = style.use(
        lambda theme: {
            "a.logo": {
                "display": "inline-flex",
                "line-height": 0,
            },
            "a.logo img": {
                "width": "auto",
                "height": "2.1rem",
                "filter": (
                    "invert(1) hue-rotate(180deg) brightness(1.15)"
                    if theme.color_scheme == "dark"
                    else "none"
                ),
            },
        }
    )

    @override
    def render(self) -> a:
        return a(
            img(src=self.attrs["logo_url"], alt="Ludic", width=240, height=66),
            href=self.attrs["home_url"],
            aria_label="Ludic home",
        )


class IconLinkAttrs(GlobalAttrs):
    to: str
    label: str


class GitHubLink(Component[NoChildren, IconLinkAttrs]):
    classes = ["icon-link"]
    styles = style.use(
        lambda theme: {
            "a.icon-link": {
                "display": "inline-flex",
                "padding": theme.sizes.xxxs,
                "border-radius": theme.rounding.normal,
                "color": theme.colors.dark,
            },
            "a.icon-link:hover": {
                "background-color": theme.colors.light,
                "text-decoration": "none",
            },
        }
    )

    @override
    def render(self) -> a:
        return a(
            GITHUB_ICON,
            href=self.attrs["to"],
            aria_label=self.attrs["label"],
            title=self.attrs["label"],
        )


class SearchBar(Component[NoChildren, GlobalAttrs]):
    classes = ["search-bar"]
    styles = style.use(
        lambda theme: {
            ".search-bar input[type=search]": {
                "inline-size": "16rem",
                "max-inline-size": "100%",
                "height": "2.4rem",
                "padding-inline": theme.sizes.s,
                "border": f"{theme.borders.thin} solid {theme.colors.light.darken(1)}",
                "border-radius": theme.rounding.normal,
                "background-color": theme.colors.light,
                "color": theme.colors.dark,
                "font-size": theme.fonts.size * 0.9,
            },
            ".search-bar input[type=search]::placeholder": {
                "color": theme.colors.dark.lighten(1),
            },
            ".search-bar input[type=search]:focus": {
                "border-color": theme.colors.primary,
                "outline": f"{theme.borders.thin} solid {theme.colors.primary}",
            },
        }
    )

    @override
    def render(self) -> InputField:
        return InputField(
            type="search",
            name="search",
            placeholder="Search the docs",
            aria_label="Search the docs",
            **self.attrs,
        )


class SiteHeaderAttrs(Attrs):
    request: Request
    active_section: str | None


class SiteHeader(Component[NoChildren, SiteHeaderAttrs]):
    """The sticky bar at the top of every page."""

    classes = ["site-header"]
    styles = style.use(
        lambda theme: {
            ".site-header > .navbar-content": {
                "max-inline-size": "90rem",
                "margin-inline": "auto",
            },
            ".site-header nav.site-nav ul": {
                "display": "flex",
                "gap": theme.sizes.xxs,
                "list-style": "none",
                "padding": "0",
            },
            ".site-header nav.site-nav li + li": {
                "margin": "0",
            },
            ".site-header nav.site-nav a": {
                "display": "inline-block",
                "padding": f"{theme.sizes.xxxxs} {theme.sizes.xs}",
                "border-radius": theme.rounding.normal,
                "color": theme.colors.dark,
                "font-weight": "500",
            },
            ".site-header nav.site-nav a:hover": {
                "background-color": theme.colors.light,
                "text-decoration": "none",
            },
            ".site-header nav.site-nav a[aria-current=page]": {
                "color": theme.colors.primary.darken(1),
            },
            ".site-header .search-bar": {
                "margin": "0",
            },
            "@media (max-width: 40rem)": {
                "header.site-header": {
                    "position": "static",
                },
                ".site-header a.logo img": {
                    "height": "1.6rem",
                },
                ".site-header > .navbar-content": {
                    "padding-inline": theme.sizes.m,
                    "gap": theme.sizes.xs,
                },
                ".site-header nav.site-nav a": {
                    "padding-inline": theme.sizes.xxxs,
                },
                ".site-header .search-bar": {
                    "flex-grow": "1",
                },
                ".site-header .search-bar input[type=search]": {
                    "inline-size": "100%",
                },
                ".site-header .header-actions": {
                    "flex-basis": "100%",
                    "flex-wrap": "nowrap",
                },
            },
        }
    )

    @override
    def render(self) -> NavBar:
        request = self.attrs["request"]
        active = self.attrs["active_section"]
        links = []
        for section in SECTIONS:
            title = "Docs" if section.name == "docs" else section.title
            url = request.url_for(f"{section.name}:index").path
            if active == section.name:
                links.append(li(a(title, href=url, aria_current="page")))
            else:
                links.append(li(a(title, href=url)))
        return NavBar(
            Cluster(
                Logo(
                    home_url=request.url_for("index").path,
                    logo_url=request.url_for("static", path="logo.png").path,
                ),
                nav(ul(*links), classes=["site-nav"], aria_label="Main"),
                classes=["small"],
            ),
            Cluster(
                SearchBar(
                    hx_post=request.url_for("search_docs").path,
                    hx_trigger="input changed delay:400ms, search",
                    hx_target="#main-content",
                    hx_select="#main-content",
                ),
                GitHubLink(to=config.GITHUB_REPO_URL, label="Ludic on GitHub"),
                ColorSchemeToggle(),
                classes=["small", "header-actions"],
            ),
        )


class Div(Block):
    classes = ["showcase"]
    styles = style.use(
        lambda theme: {
            ".showcase": {
                "color": theme.colors.primary.darken(1),
                "background-color": theme.colors.primary.lighten(1),
                "border-radius": theme.rounding.less,
                "padding-block": theme.sizes.xs,
                "text-align": "center",
            },
        }
    )


class MenuAttrs(Attrs):
    request: Request
    active_item: str | None


class Menu(Component[NoChildren, MenuAttrs]):
    """The navigation of the documentation, catalog and examples."""

    classes = ["docs-menu"]
    styles = style.use(
        lambda theme: {
            ".docs-menu li.section > a.btn": {
                "padding-inline": "0",
                "background": "none",
                "color": theme.colors.dark.darken(1),
                "font-weight": "700",
            },
            ".docs-menu li.section:not(:first-child)": {
                "margin-block-start": theme.sizes.m,
            },
            ".docs-menu li.subsection": {
                "padding-inline-start": "0",
            },
            ".docs-menu ul.stack.small > * + *": {
                "margin-block-start": "0.125rem",
            },
            ".docs-menu li.subsection a.btn": {
                "padding-block": "0.3rem",
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.925,
                "font-weight": "normal",
            },
            ".docs-menu li.subsection.active a.btn": {
                "color": theme.colors.primary.darken(1),
                "font-weight": "600",
            },
        }
    )

    @override
    def render(self) -> Navigation:
        request = self.attrs["request"]
        active = None
        if found := get_page(self.attrs["active_item"]):
            active = (found[0].name, found[1].name)

        items = []
        for section in SECTIONS:
            items.append(
                NavItem(
                    section.title,
                    to=request.url_for(f"{section.name}:index").path,
                    classes=["section"],
                )
            )
            for page in section.pages:
                items.append(
                    NavItem(
                        page.title,
                        to=request.url_for(f"{section.name}:{page.name}").path,
                        active=(section.name, page.name) == active,
                        classes=["subsection"],
                    )
                )

        return Navigation(*items, aria_label="Documentation")


class MobileMenu(Component[NoChildren, MenuAttrs]):
    """The documentation menu folded into a disclosure on narrow screens."""

    classes = ["mobile-menu"]
    styles = style.use(
        lambda theme: {
            "details.mobile-menu": {
                "border": f"{theme.borders.thin} solid {theme.colors.light.darken(1)}",
                "border-radius": theme.rounding.normal,
                "padding": f"{theme.sizes.xxs} {theme.sizes.s}",
            },
            "details.mobile-menu > summary": {
                "cursor": "pointer",
                "font-weight": "600",
            },
            "details.mobile-menu[open] > summary": {
                "margin-block-end": theme.sizes.xs,
            },
        }
    )

    @override
    def render(self) -> details:
        return details(summary("Menu"), Menu(**self.attrs))


class PageActionsAttrs(Attrs):
    request: Request
    markdown_url: str | None


class PageActions(Component[NoChildren, PageActionsAttrs]):
    """Links to edit the page on GitHub and to its Markdown version."""

    classes = ["page-actions"]
    styles = style.use(
        lambda theme: {
            "ul.page-actions": {
                "display": "flex",
                "flex-wrap": "wrap",
                "gap": f"{theme.sizes.xxxs} {theme.sizes.m}",
                "padding": "0",
                "list-style": "none",
            },
            "ul.page-actions li + li": {
                "margin": "0",
            },
            "ul.page-actions a": {
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.875,
            },
            "ul.page-actions a:hover": {
                "color": theme.colors.primary.darken(1),
            },
        }
    )

    @override
    def render(self) -> ul:
        path = self.attrs["request"].url.path.replace("-", "_")
        file_path = f"{path}index.py" if path.endswith("/") else f"{path}.py"
        edit_url = f"{config.GITHUB_REPO_WEB_URL}/blob/main/web/endpoints{file_path}"
        items = [li(a("Edit this page on GitHub", href=edit_url))]
        if markdown_url := self.attrs["markdown_url"]:
            items.append(li(a("View as Markdown", href=markdown_url)))
        return ul(*items)


class SiteFooterAttrs(Attrs):
    request: Request


class SiteFooter(Component[NoChildren, SiteFooterAttrs]):
    classes = ["site-footer"]
    styles = style.use(
        lambda theme: {
            "footer.site-footer": {
                "margin-block-start": theme.sizes.xxxxl * 2,
                "border-block-start": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                ),
                "background-color": theme.colors.light.lighten(1),
            },
            ".site-footer > .footer-content": {
                "display": "grid",
                "grid-template-columns": "repeat(auto-fit, minmax(11rem, 1fr))",
                "gap": theme.sizes.xxl,
                "max-inline-size": "90rem",
                "margin-inline": "auto",
                "padding": f"{theme.sizes.xxxl} {theme.sizes.l}",
            },
            ".site-footer .footer-brand": {
                "grid-column": "span 2",
            },
            ".site-footer .footer-brand p": {
                "margin-block-start": theme.sizes.xs,
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.9,
            },
            ".site-footer .footer-title": {
                "margin-block-end": theme.sizes.xs,
                "color": theme.colors.dark.darken(1),
                "font-size": theme.fonts.size * 0.875,
                "font-weight": "600",
            },
            ".site-footer ul": {
                "list-style": "none",
                "padding": "0",
            },
            ".site-footer li + li": {
                "margin-block-start": theme.sizes.xxxs,
            },
            ".site-footer li a": {
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.9,
            },
            ".site-footer li a:hover": {
                "color": theme.colors.primary.darken(1),
            },
            "@media (max-width: 40rem)": {
                ".site-footer .footer-brand": {
                    "grid-column": "auto",
                },
            },
        }
    )

    @override
    def render(self) -> footer:
        request = self.attrs["request"]

        def column(title: str, *links: tuple[str, str]) -> div:
            return div(
                p(title, classes=["footer-title"]),
                ul(*(li(a(text, href=url)) for text, url in links)),
            )

        return footer(
            div(
                div(
                    Logo(
                        home_url=request.url_for("index").path,
                        logo_url=request.url_for("static", path="logo.png").path,
                    ),
                    p("Typed HTML components in pure Python."),
                    p(
                        t"This site is written in Ludic and htmx. "
                        t"{a('Read its source', href=config.GITHUB_REPO_WEB_URL)}."
                    ),
                    classes=["footer-brand"],
                ),
                column(
                    "Learn",
                    ("Documentation", request.url_for("docs:index").path),
                    ("Getting Started", request.url_for("docs:getting_started").path),
                    ("Catalog", request.url_for("catalog:index").path),
                    ("Examples", request.url_for("examples:index").path),
                ),
                column(
                    "Community",
                    ("GitHub", config.GITHUB_REPO_URL),
                    ("Discord", config.DISCORD_INVITE_URL),
                    ("PyPI", "https://pypi.org/project/ludic/"),
                    ("Discussions", f"{config.GITHUB_REPO_URL}/discussions"),
                ),
                column(
                    "For coding agents",
                    ("llms.txt", request.url_for("llms_txt").path),
                    ("llms-full.txt", request.url_for("llms_full_txt").path),
                    ("Agent skills", f"{config.GITHUB_REPO_URL}/tree/main/skills"),
                    ("Context7", "https://context7.com/getludic/ludic"),
                ),
                classes=["footer-content"],
            ),
        )


class SearchResultAttrs(Attrs):
    title: AnyChildren
    content: AnyChildren
    url: str


class SearchResult(Component[NoChildren, SearchResultAttrs]):
    classes = ["search-result"]
    styles = style.use(
        lambda theme: {
            "#main-content.search-results": {
                "max-inline-size": "50rem",
                "margin-inline": "auto",
                "padding": f"{theme.sizes.xxl} {theme.sizes.l} 0",
            },
            ".docs-layout #main-content.search-results": {
                "margin-inline": "0",
                "padding": "0",
            },
            ".search-result .anchor": {
                "display": "none",
            },
            ".search-result .read-more": {
                "color": theme.colors.primary.darken(1),
                "font-weight": "600",
            },
        }
    )

    @override
    def render(self) -> Card:
        return Card(
            self.attrs["title"],
            self.attrs["content"],
            span("Read more →", classes=["read-more"]),
            to=self.attrs["url"],
        )


class QuoteAttrs(Attrs):
    source: str


class Quote(Component[str, QuoteAttrs]):
    """A testimonial quote."""

    classes = ["user-quote"]
    styles = style.use(
        lambda theme: {
            "blockquote.user-quote": {
                "padding-inline-start": theme.sizes.l,
                "border-inline-start": (
                    f"{theme.borders.thick} solid {theme.colors.primary}"
                ),
            },
            "blockquote.user-quote .quote-text": {
                "color": theme.colors.dark.darken(1),
                "font-size": theme.fonts.size * 1.15,
                "font-style": "italic",
            },
            "blockquote.user-quote .quote-source": {
                "margin-block-start": theme.sizes.xxs,
                "color": theme.colors.dark.lighten(1),
            },
        }
    )

    @override
    def render(self) -> blockquote:
        return blockquote(
            p(f"“{''.join(self.children)}”", classes=["quote-text"]),
            p(b(f"– {self.attrs['source']}"), classes=["quote-source"]),
        )
