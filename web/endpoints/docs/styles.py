from ludic.catalog.headers import H1, H2, H3, H4
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.messages import Message, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, i
from ludic.web import Request

from web.pages import Page


def styles(request: Request) -> Page:
    return Page(
        H1("Styles and Themes"),
        Paragraph(
            "There are two main ways of how to change the look and feel of your "
            "apps built with the Ludic framework:"
        ),
        List(
            Item(
                Link("CSS Styling", to="#css-styling"),
                " – you can apply custom styles to your components.",
            ),
            Item(
                Link("Themes", to="#themes"),
                " – you can change the colors, widths, fonts, etc. of your "
                "components.",
            ),
        ),
        H2("CSS Styling"),
        Paragraph(
            "There are three primary ways to apply CSS properties to components within "
            "your application:"
        ),
        NumberedList(
            Item(f"The {Code("style")} HTML Attribute"),
            Item(f"The {Code("styles")} Class Property"),
            Item(f"The {Code("style")} HTML Element"),
        ),
        H3(f"The {Code("style")} HTML Attribute"),
        Paragraph(
            "You can directly embed styles within an HTML element using the "
            f"{Code("style")} attribute. Here's an example:"
        ),
        CodeBlock(
            """
            from ludic.css import CSSProperties
            from ludic.html import form

            form(..., style=CSSProperties(color="#fff"))
            """,
            language="python",
        ),
        List(
            Item(
                f"The {Code("CSSProperties")} class is a {Code("TypedDict")} for "
                "convenience since type checkers can highlight unknown or incorrect "
                "usage."
            ),
            Item(
                "You can also use a regular Python dictionary, which might be better "
                "in most cases since CSS properties often contain hyphens:"
            ),
        ),
        CodeBlock(
            """form(..., style={"background-color": "#fff"})""",
            language="python",
        ),
        Paragraph(
            "Note that you probably want to specify the color using a theme as you can "
            f"read more about {Link("bellow", to="#themes")}."
        ),
        CodeBlock(
            """form(..., style={"background-color": theme.colors.white})""",
            language="python",
        ),
        H3(f"The {Code("styles")} Class Property"),
        Paragraph(
            f"Define CSS properties within your component using the {Code("styles")} "
            "class property. Example:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import ButtonAttrs
            from ludic.html import button
            from ludic.types import ComponentStrict


            class Button(ComponentStrict[str, ButtonAttrs]):
                classes = ["btn"]
                styles = {
                    "button.btn": {
                        "background-color": "#fab",
                        "font-size": "16px",
                    }
                }

                @override
                def render(self) -> button:
                    return button(self.children[0], **self.attrs_for(button))
            """,
            language="python",
        ),
        Message(
            Title(f"Notice the {Code("classes")} attribute"),
            f"The {Code("classes")} attribute contains the list of classes that will ",
            "be applied to the component when rendered (they will be appended if ",
            f"there are any other classes specified by the {Code("class_")} ",
            "attribute).",
        ),
        Paragraph(
            "In this case, you need to make sure you collect and render the styles. "
            f"See {Link("Collecting The Styles", to="#collecting-the-styles")} and "
            f"{Link("Integration In a Page Component",
                    to="#integration-in-a-page-component")}."
        ),
        Paragraph(
            "It is also possible to nest styles similar to how you would nest them in "
            "SCSS. The only problem is that you might get typing errors if you are "
            f"using {Code("mypy")} or {Code("pyright")}:"
        ),
        CodeBlock(
            """
            class Button(ComponentStrict[str, ButtonAttrs]):
                classes = ["btn"]
                styles = {
                    "button.btn": {
                        "color": "#eee",  # type: ignore[dict-item]
                        ".icon": {
                            "font-size": "16px",
                        }
                    }
                }
                ...
            """,
            language="python",
        ),
        Paragraph(
            f"Again, you probably want to use {i("themes")} to assign colors "
            f"(we'll talk about {i("themes")} later):"
        ),
        CodeBlock(
            """
            from ludic.html import style


            class Button(ComponentStrict[str, ButtonAttrs]):
                classes = ["btn"]
                styles = style.use(lambda theme:{
                    "button.btn": {
                        "color": theme.colors.primary,
                    }
                })
                ...
            """,
            language="python",
        ),
        H4("Collecting The Styles"),
        List(
            Item(
                Paragraph(
                    b("Load Styles: "),
                    f"Use the {Code("style.load()")} method to gather styles from all ",
                    f"components in your project. This generates a {Code("<style>")} ",
                    "element:",
                ),
                CodeBlock(
                    """
                    from ludic.html import style

                    styles = style.load()
                    """,
                    language="python",
                ),
                Paragraph(
                    f"The {Code("styles")} variable now renders as a {Code("<style>")}",
                    " element with the content similar to this:",
                ),
                CodeBlock(
                    """
                    <style>
                        button.btn { background-color: #fab; font-size: 16px; }
                    </style>
                    """,
                    language="html",
                ),
                Paragraph(
                    f"You can also pass {Code("styles.load(cache=True)")} to cache "
                    "the styles"
                ),
            ),
            Item(
                Paragraph(
                    b("Targeted Loading: "),
                    f"For more control, use {Code("style.from_components(...)")} to ",
                    "load styles from specific components:",
                ),
                CodeBlock(
                    """
                    from ludic.html import style

                    from your_app.components import Button, Form

                    styles = style.from_components(Button, Form)
                    """,
                    language="python",
                ),
            ),
        ),
        H4("Integration In a Page Component"),
        Paragraph(
            "You need to load the styles and render them in an HTML document. "
            "There are two options how to do that:"
        ),
        NumberedList(
            Item(
                f"Use the {Code("ludic.catalog.pages.HtmlPage")} component which loads "
                "the styles automatically."
            ),
            Item(
                f"Create a new {i("Page")} component and use the "
                f"{Code("style.load()")} method manually."
            ),
        ),
        Paragraph(
            f"The first method is described in the {Link(
                "getting started section",
                to=request.url_for("docs:getting_started").path)} of the "
            "documentation. Here is the second method: "
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.html import html, head, body, style
            from ludic.types import AnyChildren, Component, NoAttrs


            class Page(Component[AnyChildren, NoAttrs]):
                @override
                def render(self) -> html:
                    return html(
                        head(
                            style.load(cache=True)
                        ),
                        body(
                            ...
                        ),
                    )
            """,
            language="python",
        ),
        H4("Caching The Styles"),
        Paragraph(
            f"As mentioned before, passing {Code("cache=True")} to {Code("style.load")}"
            " caches loaded elements' styles during the first render. The problem is "
            "that the first request to your application renders the styles without the "
            "cache, so the response is a bit slower. If you want to cache the styles "
            "before your component even renders for the first time, you can use the "
            f"{Code("lifespan")} argument of the {Code("LudicApp")} class:"
        ),
        CodeBlock(
            """
            from collections.abc import AsyncIterator
            from contextlib import asynccontextmanager

            from ludic.web import LudicApp


            @asynccontextmanager
            async def lifespan(_: LudicApp) -> AsyncIterator[None]:
                style.load(cache=True)  # cache styles before accepting requests
                yield


            app = LudicApp(lifespan=lifespan)
            """,
            language="python",
        ),
        Paragraph(
            f"You can read more about {Code("Lifespan")} in {Link(
                "Starlette's documentation", to="https://www.starlette.io/lifespan/")}."
        ),
        H3(f"The {Code("style")} HTML Element"),
        Paragraph(
            f"You can also directly embed styles within a {Code("Page")} component "
            f"using the {Code("style")} element. Here's an example:"
        ),
        CodeBlock(
            """
            from ludic.html import style

            style(
                {
                    "a": {
                        "text-decoration": "none",
                        "color": "red",
                    },
                    "a:hover": {
                        "color": "blue",
                        "text-decoration": "underline",
                    },
                }
            )
            """,
            language="python",
        ),
        Paragraph("It is also possible to pass raw CSS styles as a string:"),
        CodeBlock(
            '''
            from ludic.html import style

            style("""
            .button {
                padding: 3px 10px;
                font-size: 12px;
                border-radius: 3px;
                border: 1px solid #e1e4e8;
            }
            """)
            ''',
            language="python",
        ),
        H2("Themes"),
        Paragraph(
            "You can think of themes as an option to create CSS variables, but with "
            "typing support and more flexibility."
        ),
        Paragraph("Ludic has two built-in themes: "),
        List(
            Item(Code("ludic.styles.themes.LightTheme"), " – the default theme."),
            Item(Code("ludic.styles.themes.DarkTheme"), " – the dark theme."),
        ),
        H3("How to Style Components Using Themes"),
        Paragraph(
            "Themes provide a centralized way to manage the look and feel of your "
            "components. You can directly access a component's theme to customize its "
            "styling based on your theme's settings. Here's a breakdown of how this "
            "works:"
        ),
        List(
            Item(
                b("Theme Definition: "),
                "A theme holds predefined styles like colors, fonts, and spacing. ",
                "You usually define your theme separately.",
            ),
            Item(
                b("Accessing the Theme: "),
                "Components can access the current theme through a special ",
                f"{Code("theme")} attribute. This gives you direct access to your ",
                "theme's values.",
            ),
            Item(
                b("Switching Theme: "),
                "Components can switch to a different theme by passing the component",
                f"to the {Code("theme.use()")} method. You can also switch theme ",
                "globally.",
            ),
        ),
        H3("Theme Definition"),
        Paragraph("You have two options how to create a new theme:"),
        NumberedList(
            Item(
                f"subclass {Code("Theme")} base class and define the theme's attributes"
            ),
            Item("instantiate an existing theme and override its attributes"),
        ),
        Paragraph("Here is an example of the first approach:"),
        CodeBlock(
            """
            from dataclasses import dataclass

            from ludic.styles.types import Color
            from ludic.styles.themes import Colors, Fonts, Theme


            @dataclass
            class MyTheme(Theme):
                name: str = "my-theme"

                fonts: Fonts = field(default_factory=Fonts)
                colors: Colors = field(
                    default_factory=lambda: Colors(
                        primary=Color("#c2e7fd"),
                        secondary=Color("#fefefe"),
                        success=Color("#c9ffad"),
                        info=Color("#fff080"),
                        warning=Color("#ffc280"),
                        danger=Color("#ffaca1"),
                        light=Color("#f8f8f8"),
                        dark=Color("#414549"),
                    )
                )
            """,
            language="python",
        ),
        Paragraph(
            "You can also instantiate an existing theme and override its attributes:"
        ),
        CodeBlock(
            """
            from ludic.styles.themes import Fonts, Size, LightTheme

            theme = LightTheme(fonts=Fonts(serif="serif", size=Size(1, "em")))
            """,
            language="python",
        ),
        H3("Accessing The Theme"),
        Paragraph("There are two ways to access the theme:"),
        NumberedList(
            Item(f"use the component's {Code("theme")} attribute"),
            Item(
                f"call {Code("style.use(lambda theme: { ... })")} on the component's "
                f"{Code("styles")} class attribute"
            ),
        ),
        Paragraph("Here is an example combining both approaches:"),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import ButtonAttrs
            from ludic.html import button, style
            from ludic.types import Component


            class Button(Component[str, ButtonAttrs]):
                classes = ["btn"]
                styles = style.use(lambda theme: {
                    "button.btn:hover": {
                        "background-color": theme.colors.primary.lighten(1)
                    }
                })

                @override
                def render(self) -> button:
                    return button(
                        *self.children,
                        style={
                            # Use primary color from theme
                            "background-color": self.theme.colors.primary
                        }
                    )
            """,
            language="python",
        ),
        H3("Switching Theme"),
        Paragraph("You can switch the theme globally or for a specific component:"),
        NumberedList(
            Item(
                f"use the {Code("theme.use()")} method to switch theme in a component"
            ),
            Item(
                f"use the {Code("set_default_theme()")} method to switch theme globally"
            ),
            Item(
                f"use the {Code("style.load()")} to render styles from loaded "
                "components with a different theme"
            ),
        ),
        Paragraph("Here are some examples:"),
        CodeBlock(
            """
            from ludic.attrs import GlobalAttrs
            from ludic.styles.themes import DarkTheme, LightTheme, set_default_theme
            from ludic.html import a, b, div, style
            from ludic.types import Component

            dark = DarkTheme()
            light = LightTheme()

            set_default_theme(light)

            class MyComponent(Component[str, GlobalAttrs]):
                styles = style.use(
                    # uses the theme specified by the `style.load(theme)` method
                    # or the default theme if `style.load()` was called without a theme
                    lambda theme: {
                        "#c1 a": {"color": theme.colors.warning},
                    }
                )

                @override
                def render(self) -> div:
                    return div(
                        # uses the local theme (dark)
                        dark.use(ButtonPrimary("Send")),

                        # uses the default theme (light)
                        ButtonSecondary("Cancel"),

                        # uses the default theme (light)
                        style={"background-color": self.theme.colors.primary}
                    )

            # loads styles form all components with the default theme (light)
            my_styles = style.load()

            # loads style with the specified theme (dark)
            my_styles = style.load(theme=dark)
            """,
            language="python",
        ),
        request=request,
        active_item="styles",
    )
