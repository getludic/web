from ludic.catalog.buttons import (
    Button,
    ButtonDanger,
    ButtonInfo,
    ButtonLink,
    ButtonPrimary,
    ButtonSecondary,
    ButtonSuccess,
    ButtonWarning,
)
from ludic.catalog.headers import H1, H2, H3, H4, Anchor
from ludic.catalog.items import Key, Pairs, Value
from ludic.catalog.layouts import Box, Cluster
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.loaders import Loading
from ludic.catalog.messages import (
    Message,
    MessageDanger,
    MessageInfo,
    MessageSuccess,
    MessageWarning,
    Title,
)
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, i
from ludic.web import LudicApp, Request

from web.pages import PageWithMenu

app = LudicApp()


@app.get("/catalog/")
def catalog(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Catalog"),
        Paragraph(
            f"The {Code("ludic.catalog")} module is a collection of components that "
            "might be useful for building applications with the Ludic framework."
        ),
        List(
            Item("Any contributor is welcome to add new components or helpers."),
            Item("It also serves as a showcase of possible implementations."),
        ),
        Paragraph(
            "Every item featured in the catalog is a reusable component that "
            "generates HTML code and registers its own CSS styles. The registered "
            f"CSS are loaded with the {Code("style.load()")} method as described "
            f"in the {Link("Styles and Themes", to=request.url_path_for("styles"))} "
            "section of the documentation."
        ),
        Paragraph(
            f"The catalog components are like {b("Lego pieces")} you can assemble "
            f"together to build interactive and beautiful {b("HTML documents")} "
            f"with {b("minimalistic")} approach:"
        ),
        List(
            Item(
                "You write HTML in pure Python, this removes any need for template "
                "engines and offers type safety as a bonus."
            ),
            Item(
                "The generated CSS is simple, extensible, and easy to understand. "
                "The layouts you can use for building your pages are responsive, "
                "reusable, and robust. They are based on the amazing "
                f"{Link("Every Layout Book", to="https://every-layout.dev/")}."
            ),
        ),
        H2("How Do You Use The Catalog?"),
        Paragraph(
            f"In order for everything to work correctly, the first thing you usually "
            f"need to do is to create a {Code("Page")} component. This component is "
            "important for two reasons:"
        ),
        List(
            Item(
                "It renders as a valid HTML document with (optionally) HTMX script "
                "loaded."
            ),
            Item(
                "It renders collected CSS styles loaded from the components in the "
                "catalog."
            ),
        ),
        Message(
            Title("How does CSS loading work?"),
            f"The CSS styles for components are loaded when the component is imported "
            f"anywhere in your application. The {Code("style.load()")} method iterates "
            "over all imported components and checks if the components have any styles "
            "defined.",
        ),
        Paragraph(
            "All rendered HTML documents will have this component as a base similar to "
            f"how all HTML pages in template engines like Jinja2 use the {i("base")} "
            "template."
        ),
        Message(
            Title(
                f"How does a {Code("Page")} component differ from a regular component?"
            ),
            "The only difference is that it renders as a valid HTML5 document starting "
            f"with the {Code("<!doctype html>")} declaration. You usually need only "
            f"one {Code("Page")} component in the whole application.",
        ),
        Paragraph(
            f"After you are done with setting up your {Code("Page")} component, you "
            "can use it along with all the other components in the catalog."
        ),
        H3(f"{Code("HtmlPage")} Component"),
        Paragraph(
            "This component has already been mentioned throughout the documentation "
            f"and can be used to create your {Code("Page")} component. The "
            f"{Code("HtmlPage")} component is just for convenience so that you can "
            "quickly start and not worry about how to load e.g. CSS styles or HTMX. "
        ),
        Paragraph(
            f"Here is how you would use the {Code("HtmlPage")} component to "
            f"create your own {Code("Page")} component:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import NoAttrs
            from ludic.html import link, meta
            from ludic.catalog.pages import HtmlPage, Head, Body
            from ludic.catalog.layouts import Stack
            from ludic.types import AnyChildren, Component

            class Page(Component[AnyChildren, NoAttrs]):
                @override
                def render(self) -> HtmlPage:
                    return HtmlPage(
                        Head(
                            # add custom head elements
                            meta(charset="utf-8"),
                            link(rel="icon", type="image/png", href="..."),

                            # here is a list of the Head's (optional) attributes
                            title="My Page",        # add custom title
                            favicon="favicon.ico",  # add favicon path
                            load_styles=True,       # load registered styles
                            htmx_config=...,        # configure HTMX
                        ),
                        Body(
                            # here you can create a base layout where all children of
                            # this Page component will be placed, more about layouts
                            # in the layouts section
                            Stack(*self.children),

                            # here is a list of the Body's (optional) attributes
                            htmx_version="1.9.10",  # loads HTMX script from CDN
                            htmx_path="htmx.js",    # loads HTMX script from a path
                            htmx_enabled=True,      # enable HTMX
                        ),
                    )
            """,
            language="python",
        ),
        Paragraph("Here are the default values:"),
        List(
            Item(Code("load_styles=True")),
            Item(Code('htmx_config={"defaultSwapStyle": "outerHTML"}')),
            Item(Code("htmx_enabled=True")),
            Item(Code('htmx_version="latest"')),
        ),
        Paragraph(
            f"Now that you prepared your {Code("Page")} component, you can use it in "
            "your code like here:"
        ),
        CodeBlock(
            """
            from ludic.web import LudicApp
            from ludic.catalog.buttons import Button
            from ludic.catalog.headers import H1
            from ludic.catalog.typography import Paragraph

            from your_app.pages import Page

            app = LudicApp()

            @app.get("/")
            def index(request: Request) -> Page:
                return Page(
                    H1("Hello, World!"),
                    Button("Click Me", hx_get=request.url_for("clicked")),
                )

            @app.get("/clicked")
            def clicked(request: Request) -> Paragraph:
                return Paragraph("You clicked me!")
            """,
            language="python",
        ),
        Paragraph(
            f"The {Code("HtmlPage")} component comes also with default "
            f"{Code("styles")}. In fact, the following list of styles are "
            f"auto-loaded whenever you import anything from the {Code("ludic.catalog")}"
            " module:"
        ),
        List(
            Item(Code("ludic.catalog.pages")),
            Item(Code("ludic.catalog.layouts")),
        ),
        request=request,
        active_item="catalog",
    )


@app.get("/typography/")
def typography(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Typography"),
        Paragraph(
            f"The module {Code("ludic.catalog.typography")} contains the following "
            "components:"
        ),
        H4("Link"),
        Paragraph(
            f"This text contains a {Link("link", to=str(request.url_for("catalog")))}.",
        ),
        CodeBlock(
            """
            from ludic.catalog.typography import Link

            Link("link", to="https://getludic.dev")  # appends target="_blank"
            Link("link", to="/")                     # does not append target="_blank"
            """,
            language="python",
        ),
        H4("Paragraph"),
        Paragraph("Here is some text wrapped in a paragraph."),
        CodeBlock(
            """
            from ludic.catalog.typography import Paragraph

            Paragraph("Here is some text wrapped in a paragraph.")
            """,
            language="python",
        ),
        H4("Code"),
        Paragraph(f"This text contains code: {Code("let mut x = 0;")}"),
        CodeBlock(
            """
            from ludic.catalog.typography import Code

            Code("let mut x = 0;")
            """,
            language="python",
        ),
        H4("Code Block"),
        Paragraph(
            "The following block contains a Rust code with syntax highlighting "
            "generated by Pygments:"
        ),
        CodeBlock(
            """
            fn main() {
                println!("Hello, world!");
            }
            """,
            language="rust",
        ),
        CodeBlock(
            """
            from ludic.catalog.typography import CodeBlock

            CodeBlock(
                \"\"\"
                fn main() {
                    println!("Hello, world!");
                }
                \"\"\",
                language="rust"
            )
            """,
            language="python",
        ),
        H4("Pairs"),
        CodeBlock(
            """
            from ludic.catalog.items import Pair, Key, Value

            Pairs(
                Key("First Name:"),
                Value("John"),
                Key("Last Name:"),
                Value("Doe"),
            )
            """,
            language="python",
        ),
        Pairs(
            Key("First Name:"),
            Value("John"),
            Key("Last Name:"),
            Value("Doe"),
        ),
        H4("List"),
        CodeBlock(
            """
            from ludic.catalog.lists import List, Item

            List(
                Item("A"),
                Item("B"),
                Item("C"),
            )
            """,
            language="Python",
        ),
        List(
            Item("A"),
            Item("B"),
            Item("C"),
        ),
        H4("Numbered List"),
        CodeBlock(
            """
            from ludic.catalog.lists import NumberedList, Item

            NumberedList(
                Item("One"),
                Item("Two"),
                Item("Three"),
            )
            """,
            language="Python",
        ),
        NumberedList(
            Item("One"),
            Item("Two"),
            Item("Three"),
        ),
        H2("Headers"),
        Paragraph(
            f"The module {Code("ludic.catalog.headers")} contains components "
            "rendering as HTML headers (h1-h4)."
        ),
        H1("H1", anchor=False),
        H2("H2", anchor=False),
        H3("H3", anchor=False),
        H4("H4", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.headers import H1, H2, H3, H4

            H1("H1")
            H2("H2")
            H3("H3")
            H4("H4")
            """,
            language="python",
        ),
        Paragraph(
            f"The module also contains the {Code("Anchor")} component, which can be "
            "used to create an anchor link next to the header."
        ),
        H4("H4 With Anchor", anchor=Anchor("#", target="h4-with-anchor")),
        CodeBlock(
            """
            from ludic.catalog.headers import Anchor, H4

            H4("H4 With Anchor", anchor=Anchor("#", target="h4-with-anchor"))
            """,
            language="python",
        ),
        Paragraph(
            "It is possible to generate the anchor automatically using the "
            f"{Code("anchor=True")} attribute:"
        ),
        H3("H3 With Anchor", anchor=True),
        CodeBlock(
            """
            from ludic.catalog.headers import H3

            H3("H3 With Anchor", anchor=True)
            """,
            language="python",
        ),
        request=request,
        active_item="typography",
    )


@app.get("/buttons/")
def buttons(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Buttons"),
        Paragraph(
            f"The module {Code("ludic.catalog.buttons")} contains the following "
            "buttons (the name is the same):"
        ),
        Box(
            Cluster(
                Button("Button"),
                ButtonPrimary("ButtonPrimary"),
                ButtonSecondary("ButtonSecondary"),
                ButtonSuccess("ButtonSuccess"),
                ButtonInfo("ButtonInfo"),
                ButtonWarning("ButtonWarning"),
                ButtonDanger("ButtonDanger"),
                ButtonLink("ButtonLink"),
                classes=["centered"],
            ),
        ),
        CodeBlock(
            """
            from ludic.catalog.buttons import (
                Button, ButtonPrimary, ButtonSecondary, ButtonSuccess, ButtonInfo,
                ButtonWarning, ButtonDanger, ButtonLink
            )

            Button("Button")
            ButtonPrimary("ButtonPrimary")
            ButtonSecondary("ButtonSecondary")
            ButtonSuccess("ButtonSuccess")
            ButtonInfo("ButtonInfo")
            ButtonWarning("ButtonWarning")
            ButtonDanger("ButtonDanger")
            ButtonLink("ButtonLink")
            """,
            language="python",
        ),
        H2("Button Sizes"),
        Paragraph(
            "You can also change the size of the button appending the "
            f"{Code("small")} or {Code("large")} class:"
        ),
        Box(
            Cluster(
                ButtonPrimary("Small", classes=["small"]),
                ButtonPrimary("Normal"),
                ButtonPrimary("Large", classes=["large"]),
                classes=["centered"],
            )
        ),
        CodeBlock(
            """
            from ludic.catalog.buttons import ButtonPrimary

            ButtonPrimary("Small", classes=["small"])
            ButtonPrimary("Normal")
            ButtonPrimary("Large", classes=["large"])
            """,
            language="python",
        ),
        request=request,
        active_item="buttons",
    )


@app.get("/messages/")
def messages(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Messages"),
        Paragraph(
            f"The module {Code("ludic.catalog.messages")} contains the following "
            "components:"
        ),
        Message(
            Title("Message"),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi.",
        ),
        MessageSuccess(
            Title("MessageSuccess"),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi.",
        ),
        MessageInfo(
            Title("MessageInfo"),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi.",
        ),
        MessageWarning(
            Title("MessageWarning"),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi.",
        ),
        MessageDanger(
            Title("MessageDanger"),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi.",
        ),
        CodeBlock(
            """
            from ludic.catalog.messages import (
                Message, MessageSuccess, MessageInfo, MessageWarning, MessageDanger,
            )

            Message(Title("Message"), "...")
            MessageSuccess(Title("MessageSuccess"), "...")
            MessageInfo(Title("MessageInfo"), "...")
            MessageWarning(Title("MessageWarning"), "...")
            MessageDanger(Title("MessageDanger"), "...")
            """,
            language="python",
        ),
        Paragraph(
            f"Note that you don't need to specify the {Code("Title")} component. "
            "Here is how the message renders without the title:"
        ),
        Message(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        ),
        request=request,
        active_item="messages",
    )


@app.get("/loaders/")
def loaders(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Loaders"),
        Paragraph(
            "Loaders help load content asynchronously when the HTML page is rendered. "
            "The module currently contains only one loader requiring HTMX enabled."
        ),
        H4("Lazy Loader"),
        CodeBlock(
            """
            from ludic.catalog.loaders import LazyLoader

            LazyLoader(load_url="https://example.com/huge-image.png")
            """,
            language="python",
        ),
        Paragraph(
            "The default placeholder displayed before the content is loaded looks like "
            "this:"
        ),
        Loading(),
        Paragraph("However, you can use your own placeholder:"),
        CodeBlock(
            """
            from ludic.catalog.loaders import LazyLoader, Loading

            LazyLoader(
                load_url="https://example.com/huge-image.png",
                placeholder=Loading(),  # replace with your own placeholder
            )
            """,
            language="python",
        ),
        request=request,
        active_item="loaders",
    )
