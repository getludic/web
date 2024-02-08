from typing import override

from ludic.html import div, img
from ludic.types import Attrs, Component, NoChildren


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
