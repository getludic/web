from typing import override

from ludic.attrs import Attrs, GlobalAttrs, NoAttrs
from ludic.base import AnyChildren
from ludic.catalog.buttons import ButtonLink
from ludic.catalog.forms import InputField
from ludic.catalog.layouts import Box, Cluster, Stack, Switcher
from ludic.catalog.navigation import Navigation, NavItem
from ludic.catalog.typography import Link
from ludic.html import a, b, div, iframe, img, style
from ludic.types import Component, NoChildren
from ludic.web import Request
from ludic.web.datastructures import URLPath

from . import config


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


class LogoBigAttrs(Attrs):
    logo_url: str


class LogoBig(Component[NoChildren, LogoBigAttrs]):
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


class MainHeaderAttrs(Attrs):
    home_url: str
    logo_url: str
    search_url: str


class LogoAttrs(Attrs):
    home_url: str
    logo_url: str


class Logo(Component[NoChildren, LogoAttrs]):
    @override
    def render(self) -> a:
        return a(
            img(src=self.attrs["logo_url"], alt="Ludic Logo", style={"width": "8rem"}),
            href=self.attrs["home_url"],
            style={"line-height": "0"},
        )


class GitHubButton(Component[NoChildren, NoAttrs]):
    @override
    def render(self) -> iframe:
        return iframe(
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
            width="140px",
            height="30px",
            title="GitHub",
        )


class MainHeader(Component[AnyChildren, MainHeaderAttrs]):
    classes = ["main-header"]
    styles = {
        ".main-header .switcher > :nth-child(2)": {
            "flex-grow": "3",
        },
    }

    @override
    def render(self) -> Box:
        return Box(
            Switcher(
                Cluster(
                    Logo(
                        home_url=self.attrs["home_url"],
                        logo_url=self.attrs["logo_url"],
                    )
                ),
                SearchBar(
                    hx_post=self.attrs["search_url"],
                    hx_trigger="input changed delay:500ms, search",
                    hx_target="#main-content",
                    hx_select="#main-content",
                ),
                Cluster(
                    GitHubButton(),
                    classes=["flex-end"],
                ),
            ),
        )


class HomeHeaderAttrs(Attrs):
    home_url: str
    logo_url: str
    docs_url: str
    catalog_url: str
    examples_url: str


class HomeHeader(Component[AnyChildren, HomeHeaderAttrs]):
    classes = ["cover-header"]

    @override
    def render(self) -> Box:
        return Box(
            Cluster(
                Logo(
                    home_url=self.attrs["home_url"],
                    logo_url=self.attrs["logo_url"],
                ),
                Cluster(
                    ButtonLink("Documentation", to=self.attrs["docs_url"]),
                    ButtonLink("Catalog", to=self.attrs["catalog_url"]),
                    ButtonLink("Examples", to=self.attrs["examples_url"]),
                    GitHubButton(),
                ),
                classes=["justify-space-between"],
            )
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
    SECTIONS = {
        "docs": "Documentation",
        "catalog": "Catalog",
        "examples": "Examples",
    }
    SUBSECTIONS = {
        "docs": {
            "index": "Introduction",
            "getting_started": "Getting Started",
            "components": "Components",
            "styles": "Styles and Themes",
            "htmx": "HTMX Support",
            "web_framework": "Web Framework",
        },
        "catalog": {
            "index": "Basics",
            "layouts": "Layouts",
            "typography": "Typography",
            "buttons": "Buttons",
            "messages": "Messages",
            "forms": "Forms",
            "tables": "Tables",
            "loaders": "Loaders",
        },
        "examples": {
            "index": "Components",
            "bulk_update": "Bulk Update",
            "click_to_edit": "Click to Edit",
            "click_to_load": "Click to Load",
            "delete_row": "Delete Row",
            "edit_row": "Edit Row",
            "infinite_scroll": "Infinite Scroll",
            "lazy_loading": "Lazy Loading",
        },
    }

    @override
    def render(self) -> Box:
        request = self.attrs["request"]

        if active_item := self.attrs.get("active_item"):
            parts = active_item.split(":", 1)
        else:
            parts = [""]

        if len(parts) == 2:
            active_section, active_subsection = parts
        else:
            active_section, active_subsection = None, parts[0]

        items = []

        for section, subsections in self.SUBSECTIONS.items():
            in_subsection = (
                active_section is None or active_section == section
            ) and active_subsection in subsections

            items.append(
                NavItem(
                    self.SECTIONS[section],
                    to=request.url_for(f"{section}:index").path,
                    active_subsection=in_subsection,
                    classes=["section"],
                )
            )
            if in_subsection:
                for item in subsections:
                    items.append(
                        NavItem(
                            subsections[item],
                            to=request.url_for(f"{section}:{item}").path,
                            active=active_subsection == item,
                            classes=["subsection"],
                        )
                    )

        return Box(Navigation(*items, hx_boost=True))


class Footer(Component[NoChildren, NoAttrs]):
    classes = ["text-align-center"]

    @override
    def render(self) -> Box:
        return Box(
            f"Made with {b(Link("Ludic", to=config.GITHUB_REPO_URL))} "
            f"and {b(Link("HTMX", to="https://htmx.org"))}"
        )


class SearchBar(Component[NoChildren, GlobalAttrs]):
    classes = ["search-bar"]
    styles = style.use(
        lambda theme: {
            ".search-bar": {
                'input[type="search"]': {
                    "background-color": theme.colors.light,
                    "border": f"1px solid {theme.colors.light.darken(5)}",
                    "border-radius": theme.rounding.less,
                    "font-size": theme.fonts.size * 0.9,
                    "height": "auto",
                    "color": theme.colors.dark,
                    "transition": "all 0.3s ease-in-out",
                },
                'input[type="search"]::placeholder': {
                    "color": theme.colors.dark.lighten(7),
                },
                'input[type="search"]:focus': {
                    "border-color": theme.colors.dark.lighten(5),
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


class EditOnGithubAttrs(Attrs):
    base_url: URLPath


class EditOnGithub(Component[NoChildren, EditOnGithubAttrs]):
    classes = ["edit-on-github"]
    styles = style.use(
        lambda theme: {
            ".edit-on-github": {
                "position": "relative",
            },
            ".edit-on-github a": {
                "float": "right",
                "position": "absolute",
                "z-index": "10",
                "right": "0",
                "color": theme.colors.dark,
            },
        }
    )

    @override
    def render(self) -> div:
        file_path = (
            f"{self.attrs["base_url"].replace("-", "_")}index.py"
            if self.attrs["base_url"].endswith("/")
            else f"{self.attrs["base_url"].replace("-", "_")}.py"
        )
        url = f"{config.GITHUB_REPO_WEB_URL}/blob/main/web/endpoints{file_path}"
        return div(
            ButtonLink("Edit Page", to=url, classes=["small"]),
            style={"position": "relative"},
        )
