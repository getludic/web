from ludic.catalog.headers import H1, H2, H3, H4
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.messages import Message, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, i
from ludic.web import Request

from web.pages import Page


def styles(request: Request) -> Page:
    themes_url = request.url_path_for("docs:themes")
    return Page(
        H1("Styles"),
        Paragraph(
            t"This page describes how to add CSS to your components. To change the "
            t"colors, fonts and sizes of your app, including the catalog "
            t"components, change the theme, see {Link('Themes', to=themes_url)}."
        ),
        H2("CSS Styling"),
        Paragraph(
            "There are three primary ways to apply CSS properties to components within "
            "your application:"
        ),
        NumberedList(
            Item(t"The {Code('style')} HTML Attribute"),
            Item(t"The {Code('styles')} Class Property"),
            Item(t"The {Code('style')} HTML Element"),
        ),
        H3(t"The {Code('style')} HTML Attribute"),
        Paragraph(
            t"You can directly embed styles within an HTML element using the "
            t"{Code('style')} attribute. Here's an example:"
        ),
        CodeBlock(
            """
            from ludic.styles import CSSProperties
            from ludic.html import form

            form(..., style=CSSProperties(color="#fff"))
            """,
            language="python",
        ),
        List(
            Item(
                t"The {Code('CSSProperties')} class is a {Code('TypedDict')} for "
                t"convenience since type checkers can highlight unknown or incorrect "
                t"usage."
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
            t"You probably want to take the color from the "
            t"{Link('theme', to=themes_url)}:"
        ),
        CodeBlock(
            """form(..., style={"background-color": theme.colors.white})""",
            language="python",
        ),
        H3(t"The {Code('styles')} Class Property"),
        Paragraph(
            t"Define CSS properties within your component using the {Code('styles')} "
            t"class property. Example:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import ButtonAttrs
            from ludic.html import button
            from ludic.components import ComponentStrict


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
            Title(t"Notice the {Code('classes')} attribute"),
            t"The {Code('classes')} attribute contains the list of classes that will ",
            "be applied to the component when rendered (they will be appended if ",
            t"there are any other classes specified by the {Code('class_')} ",
            "attribute).",
        ),
        Paragraph(
            t"In this case, you need to make sure you collect and render the styles. "
            t"See {Link('Collecting The Styles', to='#collecting-the-styles')} and "
            t"{
                Link(
                    'Integration In a Page Component',
                    to='#integration-in-a-page-component',
                )
            }."
        ),
        Paragraph(
            t"It is also possible to nest styles similar to how you would nest them in "
            t"SCSS. The only problem is that you might get typing errors if you are "
            t"using {Code('mypy')} or {Code('pyright')}:"
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
            t"Again, you probably want to take the colors from the "
            t"{Link('theme', to=themes_url)}:"
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
                    t"Use the {Code('style.load()')} method to gather styles from all ",
                    t"components in your project. This generates a {Code('<style>')} ",
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
                    t"The {Code('styles')} variable now renders as a {Code('<style>')}",
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
                    t"You can also pass {Code('styles.load(cache=True)')} to cache "
                    t"the styles"
                ),
            ),
            Item(
                Paragraph(
                    b("Targeted Loading: "),
                    t"For more control, use {Code('style.from_components(...)')} to ",
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
                t"Use the {Code('ludic.catalog.pages.HtmlPage')} component which loads "
                t"the styles automatically."
            ),
            Item(
                t"Create a new {i('Page')} component and use the "
                t"{Code('style.load()')} method manually."
            ),
        ),
        Paragraph(
            t"The first method is described in the {
                Link(
                    'catalog section',
                    to=f'{request.url_for("catalog:index").path}#htmlpage-component',
                )
            } "
            t"of the documentation. Here is the second method: "
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import NoAttrs
            from ludic.html import html, head, body, style
            from ludic.components import Component
            from ludic.types import AnyChildren


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
            t"As mentioned before, passing {Code('cache=True')} to {Code('style.load')}"
            t" caches loaded elements' styles during the first render. The problem is "
            t"that the first request to your application renders the styles without "
            t"the cache, so the response is a bit slower. If you want to cache the "
            t"styles before your component even renders for the first time, you can "
            t"use the {Code('lifespan')} argument of the {Code('LudicApp')} class:"
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
            t"You can read more about {Code('Lifespan')} in {
                Link(
                    "Starlette's documentation", to='https://www.starlette.io/lifespan/'
                )
            }."
        ),
        H3(t"The {Code('style')} HTML Element"),
        Paragraph(
            t"You can also directly embed styles within a {Code('Page')} component "
            t"using the {Code('style')} element. Here's an example:"
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
        request=request,
        active_item="styles",
        title="Ludic - Styles",
    )
