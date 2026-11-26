from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.lists import Item, List
from ludic.catalog.messages import Message, Title
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import span
from ludic.web import Request

from web import config
from web.pages import Page

THEMES_SOURCE_URL = f"{config.GITHUB_REPO_URL}/blob/main/ludic/styles/themes.py"


def themes(request: Request) -> Page:
    return Page(
        H1("Themes"),
        Paragraph(
            "A theme holds the colors, fonts and sizes of your app and the settings "
            "of the catalog components. Components read the theme when Ludic "
            "renders their styles, so a change in the theme restyles every "
            "component that uses it, without any CSS."
        ),
        Paragraph(
            t"Ludic has two themes in {Code('ludic.styles.themes')}: "
            t"{Code('LightTheme')}, the default, and {Code('DarkTheme')}."
        ),
        H2("Create a Theme"),
        Paragraph(
            t"Subclass {Code('LightTheme')} or {Code('DarkTheme')} as a dataclass, "
            t"give it a new name and override the fields you want to change. A field "
            t"that holds another dataclass, such as {Code('colors')}, needs a "
            t"{Code('default_factory')}:"
        ),
        CodeBlock(
            """
            from dataclasses import dataclass, field

            from ludic.styles import themes
            from ludic.styles.types import ColorRange


            @dataclass
            class BrandTheme(themes.LightTheme):
                name: str = "brand"

                colors: themes.Colors = field(
                    default_factory=lambda: themes.Colors(
                        primary=ColorRange(["#1e3a8a", "#1d4ed8", "#dbeafe"]),
                    )
                )
                fonts: themes.Fonts = field(
                    default_factory=lambda: themes.Fonts(
                        primary="Inter, sans-serif",
                        secondary="Inter, sans-serif",
                    )
                )
            """,
            language="python",
        ),
        Paragraph("For a small change, create a theme with keyword arguments:"),
        CodeBlock(
            """
            from ludic.styles import themes
            from ludic.styles.types import Color

            theme = themes.LightTheme(
                name="brand",
                buttons=themes.Buttons(
                    color=Color("#1d4ed8"), background_color=Color("#dbeafe")
                ),
            )
            """,
            language="python",
        ),
        Message(
            Title("Give every theme its own name"),
            "Ludic caches the rendered styles by the name of the theme, so two "
            "themes with the same name would share their styles.",
        ),
        H2("Apply a Theme"),
        Paragraph(
            t"Make your theme the default when the app starts, with "
            t"{Code('set_default_theme')}. All components then use it:"
        ),
        CodeBlock(
            """
            from ludic.styles.themes import set_default_theme
            from ludic.web import LudicApp

            from my_app.themes import BrandTheme

            set_default_theme(BrandTheme())

            app = LudicApp()
            """,
            language="python",
        ),
        Paragraph(
            t"Set the default theme even when you also pass the theme to "
            t"{Code('Head(theme=...)')}. {Code('Head')} renders the collected styles "
            t"with it, but the styles that components compute while they render "
            t"come from the default theme. For example, {Code('CodeBlock')} picks "
            t"the colors of highlighted code and of line numbers this way."
        ),
        H3("Dark Mode"),
        Paragraph(
            t"Pass a second theme to {Code('Head')} as {Code('dark_theme')}. Its "
            t"styles apply when the visitor's system is in dark mode, and "
            t"{Code('ColorSchemeToggle')} lets the visitor switch by hand. The "
            t"browser remembers the choice."
        ),
        CodeBlock(
            """
            from ludic.catalog.pages import Body, ColorSchemeToggle, Head, HtmlPage
            from ludic.catalog.typography import Paragraph
            from ludic.styles.themes import DarkTheme, LightTheme, set_default_theme

            light = LightTheme()
            dark = DarkTheme()
            set_default_theme(light)

            page = HtmlPage(
                Head(title="My App", theme=light, dark_theme=dark),
                Body(ColorSchemeToggle(), Paragraph("Hello!")),
            )
            """,
            language="python",
        ),
        Paragraph(
            t"The styles that components compute while they render come from the "
            t"default theme in both schemes. Keep the settings they read the same "
            t"in both themes, e.g. give both themes the same {Code('code')} "
            t"settings with a dark background."
        ),
        H3("A Part of a Page"),
        Paragraph(
            t"{Code('theme.use(element)')} sets the theme that {Code('self.theme')} "
            t"returns in the element and its children. It does not change the "
            t"collected styles, which the page renders once with its own theme."
        ),
        H2("Settings"),
        Paragraph(
            t"These are the fields of a theme. Their default values are in "
            t"{Link('ludic/styles/themes.py', to=THEMES_SOURCE_URL)}."
        ),
        Table(
            TableHead("Field", "What it changes"),
            TableRow(
                Code("measure"),
                span(t"The maximum width of text, {Code('70ch')} by default."),
            ),
            TableRow(
                Code("line_height"),
                span(
                    t"The line height of the page, {Code('1.5')}. Headings use 90 % "
                    t"of it."
                ),
            ),
            TableRow(
                Code("color_scheme"),
                span(
                    t"{Code('light')} or {Code('dark')}: the CSS "
                    t"{Code('color-scheme')} of the page and the icon of "
                    t"{Code('ColorSchemeToggle')}."
                ),
            ),
            TableRow(Code("colors"), Link("Colors", to="#colors")),
            TableRow(Code("fonts"), Link("Fonts", to="#fonts")),
            TableRow(
                Code("sizes"),
                span(
                    t"The spacing scale from {Code('xxxxs')} to {Code('xxxxl')}. The "
                    t"catalog uses it for padding, gaps and margins."
                ),
            ),
            TableRow(
                Code("borders"),
                span(
                    t"Border widths: {Code('thin')}, {Code('normal')} and "
                    t"{Code('thick')}."
                ),
            ),
            TableRow(
                Code("rounding"),
                span(
                    t"Border radius: {Code('less')}, {Code('normal')} and "
                    t"{Code('more')}."
                ),
            ),
            TableRow(Code("headers"), Link("Headers", to="#headers")),
            TableRow(Code("layouts"), Link("Layouts", to="#layouts")),
            TableRow(Code("code"), Link("Code blocks", to="#code-blocks")),
            TableRow(Code("buttons"), Link("Buttons", to="#buttons")),
        ),
        H3("Colors"),
        Paragraph(t"The {Code('Colors')} dataclass:"),
        Table(
            TableHead("Field", "What it changes"),
            TableRow(
                Code("primary"),
                span(
                    t"Links, {Code('ButtonPrimary')}, the active tab and navigation "
                    t"item, and inline code."
                ),
            ),
            TableRow(
                span(
                    t"{Code('secondary')}, {Code('success')}, {Code('info')}, "
                    t"{Code('warning')}, {Code('danger')}"
                ),
                span(
                    t"The variants of buttons and messages, e.g. "
                    t"{Code('ButtonDanger')} or {Code('MessageSuccess')}."
                ),
            ),
            TableRow(
                Code("white"),
                "The background of the page, cards, messages and form fields.",
            ),
            TableRow(Code("dark"), "The color of text."),
            TableRow(
                Code("light"),
                "The background of default buttons, inline code and navigation "
                "items, and in darker shades the borders.",
            ),
            TableRow(Code("black"), "The text of default buttons."),
        ),
        Paragraph(
            t"In a dark theme, {Code('white')} is the dark background and "
            t"{Code('dark')} the light text. The names describe the role of the "
            t"color in the light theme."
        ),
        H3("Fonts"),
        Table(
            TableHead("Field", "What it changes"),
            TableRow(Code("primary"), "The font of text."),
            TableRow(Code("secondary"), "The font of headings."),
            TableRow(Code("monospace"), "The font of code."),
            TableRow(
                Code("size"),
                span(
                    t"The base font size, {Code('1em')}. Other font sizes are relative "
                    t"to it."
                ),
            ),
        ),
        H3("Headers"),
        Paragraph(
            t"{Code('headers.h1')} to {Code('headers.h6')} are a {Code('Header')} "
            t"with the font {Code('size')} and {Code('anchor')}. With "
            t"{Code('anchor=True')}, the catalog headers {Code('H1')} to "
            t"{Code('H4')} get an id and a link to themselves:"
        ),
        CodeBlock(
            """
            from ludic.styles import themes
            from ludic.styles.types import SizeClamp

            theme = themes.LightTheme(
                name="anchors",
                headers=themes.Headers(
                    h2=themes.Header(size=SizeClamp(1.5, 1.3, 2.8), anchor=True),
                ),
            )
            """,
            language="python",
        ),
        H3("Layouts"),
        Paragraph(
            t"{Code('layouts')} configures the {
                Link('layouts', to=request.url_path_for('catalog:layouts'))
            } of the catalog:"
        ),
        Table(
            TableHead("Field", "What it changes"),
            TableRow(
                Code("sidebar.side_width"),
                span(
                    t"The width of the sidebar in {Code('WithSidebar')}. With "
                    t"{Code('None')}, the default, the sidebar is as wide as its "
                    t"content."
                ),
            ),
            TableRow(
                Code("sidebar.content_min_width"),
                span(
                    t"The narrowest the content can be before the sidebar wraps above "
                    t"it, {Code('60%')}."
                ),
            ),
            TableRow(
                Code("switcher.threshold"),
                span(
                    t"The width of the container at which {Code('Switcher')} switches "
                    t"between a row and a column, {Code('40rem')}."
                ),
            ),
            TableRow(
                Code("switcher.limit"),
                span(
                    t"The most elements {Code('Switcher')} shows in a row, {Code('4')}."
                ),
            ),
            TableRow(
                Code("cover.min_height"),
                span(t"The minimum height of {Code('Cover')}, {Code('100vh')}."),
            ),
            TableRow(
                Code("cover.element"),
                span(
                    t"The selector of the child that {Code('Cover')} centers "
                    t"vertically, {Code('h1')}."
                ),
            ),
            TableRow(
                Code("grid.cell_size"),
                span(t"The minimum width of a {Code('Grid')} cell, {Code('250px')}."),
            ),
            TableRow(
                span(t"{Code('frame.numerator')}, {Code('frame.denominator')}"),
                span(t"The aspect ratio of {Code('Frame')}, {Code('16:9')}."),
            ),
        ),
        CodeBlock(
            """
            from ludic.styles import themes
            from ludic.styles.types import Size

            theme = themes.LightTheme(
                name="wide-sidebar",
                layouts=themes.Layouts(
                    sidebar=themes.Sidebar(side_width="20rem"),
                    grid=themes.Grid(cell_size=Size(18, "rem")),
                ),
            )
            """,
            language="python",
        ),
        H3("Code Blocks"),
        Paragraph(t"{Code('code')} configures {Code('CodeBlock')}:"),
        Table(
            TableHead("Field", "What it changes"),
            TableRow(
                span(t"{Code('color')}, {Code('background_color')}"), "The colors."
            ),
            TableRow(Code("line_number_color"), "The color of line numbers."),
            TableRow(
                Code("line_numbers"),
                span(
                    t"Whether code blocks have line numbers, {Code('True')}. A code "
                    t"block can override it with {Code('line_numbers=False')}."
                ),
            ),
            TableRow(Code("font_size"), span(t"The font size, {Code('0.9rem')}.")),
            TableRow(
                Code("style"),
                span(
                    t"The {Link('Pygments style', to='https://pygments.org/styles/')} "
                    t"that highlights the code: a name, e.g. {Code('github-dark')}, or "
                    t"a style class."
                ),
            ),
        ),
        CodeBlock(
            """
            from ludic.styles import themes
            from ludic.styles.types import Color

            theme = themes.LightTheme(
                name="dark-code",
                code=themes.CodeBlock(
                    color=Color("#e2e8f0"),
                    background_color=Color("#0f172a"),
                    line_number_color=Color("#64748b"),
                    style="github-dark",
                ),
            )
            """,
            language="python",
        ),
        Paragraph(
            t"The catalog component {Code('CodeBlock')} and the theme's "
            t"{Code('CodeBlock')} share the name. Import the theme's one through "
            t"the module, as {Code('themes.CodeBlock')}."
        ),
        H3("Buttons"),
        Paragraph(
            t"{Code('buttons')} sets the {Code('color')} and "
            t"{Code('background_color')} of the default {Code('Button')} and of "
            t"{Code('ButtonLink')}. Without them, the default button has the "
            t"background of {Code('colors.light')} and the text of "
            t"{Code('colors.black')}. The other buttons, such as "
            t"{Code('ButtonPrimary')}, take their colors from {Code('colors')}."
        ),
        H2("Colors and Sizes"),
        Paragraph(
            t"The values in a theme are strings, so you can use them anywhere CSS "
            t"expects a color or a size. The classes in {Code('ludic.styles.types')} "
            t"add a few helpers."
        ),
        H3("Color and ColorRange"),
        List(
            Item(
                t"{Code('Color("#0f766e")')} is a color. {Code('darken(n)')} and "
                t"{Code('lighten(n)')} return a darker or lighter shade, and "
                t"{Code('readable()')} returns black or white, whichever is "
                t"readable on the color."
            ),
            Item(
                t"{Code('ColorRange([...])')} is a list of variants of one color, from "
                t"the darkest to the lightest. It is the middle variant, and "
                t"{Code('darken(n)')} and {Code('lighten(n)')} move {Code('n')} steps "
                t"along the list. The colors of the built-in themes are ranges."
            ),
        ),
        CodeBlock(
            """
            from ludic.styles.types import Color, ColorRange

            primary = ColorRange(["#0b5f59", "#0f766e", "#ccfbf1"])
            primary             # "#0f766e"
            primary.darken()    # "#0b5f59"
            primary.lighten()   # "#ccfbf1"
            primary.readable()  # "#fff"

            Color("#0f766e").darken()  # "#0e7068"
            """,
            language="python",
        ),
        H3("Size and SizeClamp"),
        List(
            Item(
                t"{Code('Size(1.5)')} is a size in {Code('rem')}, or in the unit you "
                t"pass. Multiplying, adding and subtracting a number keeps the unit."
            ),
            Item(
                t"{Code('SizeClamp(minimum, value, maximum)')} is a size that grows "
                t"with the width of the window: from {Code('minimum')} rem, by "
                t"{Code('value')} vw, up to {Code('maximum')} rem. It renders as the "
                t"CSS {Code('clamp()')}, and arithmetic changes all three numbers."
            ),
        ),
        CodeBlock(
            """
            from ludic.styles.types import Size, SizeClamp

            Size(1.5)       # "1.5rem"
            Size(1.5) * 2   # "3rem"
            Size(70, "ch")  # "70ch"

            SizeClamp(1, 0.3, 1.16)      # "clamp(1rem, 1rem + 0.3vw, 1.16rem)"
            SizeClamp(1, 0.3, 1.16) * 2  # "clamp(2rem, 2rem + 0.6vw, 2.32rem)"
            """,
            language="python",
        ),
        H2("Use the Theme in Your Components"),
        Paragraph(
            t"Read the theme in the {Code('styles')} of a component with "
            t"{Code('style.use')}. Ludic renders these styles with the theme of the "
            t"page, so they also switch with the dark theme:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import GlobalAttrs
            from ludic.components import Component
            from ludic.html import div, style
            from ludic.types import AnyChildren


            class Callout(Component[AnyChildren, GlobalAttrs]):
                classes = ["callout"]
                styles = style.use(
                    lambda theme: {
                        ".callout": {
                            "background-color": theme.colors.primary.lighten(),
                            "color": theme.colors.primary.darken(),
                            "padding": theme.sizes.m,
                            "border-radius": theme.rounding.normal,
                        }
                    }
                )

                @override
                def render(self) -> div:
                    return div(*self.children, **self.attrs)
            """,
            language="python",
        ),
        Paragraph(
            t"In {Code('render()')}, the theme is {Code('self.theme')}. Inline "
            t"styles computed from it do not switch with the dark theme, so prefer "
            t"{Code('styles')} for colors. The {
                Link('Styles', to=request.url_path_for('docs:styles'))
            } page describes how the styles of components are collected."
        ),
        request=request,
        active_item="themes",
        title="Ludic - Themes",
    )
