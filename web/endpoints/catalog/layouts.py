from ludic.catalog.buttons import (
    Button,
    ButtonDanger,
    ButtonInfo,
    ButtonLink,
    ButtonPrimary,
    ButtonSuccess,
)
from ludic.catalog.headers import H1, H2, H3, H4
from ludic.catalog.layouts import (
    Box,
    Center,
    Cluster,
    Cover,
    Frame,
    Grid,
    Sidebar,
    Stack,
    Switcher,
    WithSidebar,
)
from ludic.catalog.lists import Item, List
from ludic.catalog.messages import Message, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, div, h1
from ludic.web import Request

from web.components import Div
from web.pages import BasePage, Page


def layouts(request: Request) -> Page:
    return Page(
        H1("Layouts"),
        Paragraph(
            "Layouts create a flexible structure for your user interface. "
            f"The layouts in this module are based on the {b("Every Layout Book")}. "
            "If you haven't read the book, go read it now: "
        ),
        List(Item(Link("Every Layout Book", to="https://every-layout.dev/"))),
        Paragraph(
            "These layouts allow us to create complex user interfaces with "
            "minimal CSS which are responsive and readable on all devices. "
            "The layouts can be combined together."
        ),
        Paragraph(
            f"All layouts are located in the {Code("ludic.catalog.layouts")} module."
        ),
        Message(
            Title("Viewing this page on mobile devices"),
            "If you are viewing this page on mobile devices, you won't probably see "
            "the layouts examples correctly rendered. You can always switch between "
            "desktop mode and mobile if you want to see the difference in rendering.",
        ),
        H2("Ideology"),
        Paragraph(
            "In this module, layouts are designed as simple, reusable components that "
            "you can easily combine to create responsive, readable, and maintainable "
            "user interfaces. Instead of starting from scratch with basic HTML "
            "elements and manually writing CSS, you use these layouts as your "
            f"{b("foundational building blocks")}. This approach allows you to compose "
            "and arrange them in various ways to design your desired user interface, "
            "making your code more organized and easier to manage."
        ),
        b("A New Way of Thinking About Design"),
        Paragraph(
            "When writing CSS, you might be tempted to apply e.g. specific spacing, "
            "colors, or font styles to an HTML element like a button. The idea of "
            f"using the layout classes here is to define {b("context")} which "
            "determines how an HTML element should be displayed. So for example, we "
            "might want to have a couple of buttons on one line, so we wrap them in "
            "a Cluster class which inserts a margin between all its children and puts "
            "them on one line. In another context, we want to widen a button so that "
            "it uses all available space and is displayed like a block element. In "
            "that case we use the Stack class."
        ),
        Paragraph("To illustrate this concept, here is a button wrapped in a Cluster:"),
        Cluster(Button("In a Cluster"), Button("In a Cluster")),
        Paragraph("Here are the buttons wrapped in a Stack:"),
        Stack(Button("In a Stack"), Button("In a Stack")),
        Paragraph("Let's see the code:"),
        CodeBlock(
            """
            from ludic.catalog.buttons import Button
            from ludic.catalog.layouts import Cluster, Stack

            Cluster(Button("In a Cluster"), Button("In a Cluster"))
            Stack(Button("In a Stack"), Button("In a Stack"))
            """,
            language="python",
        ),
        H2("Stack"),
        Paragraph(
            "In the Stack layout, there's margin inserted between all its children "
            "elements, and each child occupies all the available horizontal space. "
            "So, essentially, each child stretches out horizontally as much as "
            "possible, with margins separating them."
        ),
        H4("Example", anchor=False),
        Stack(
            Div("One"),
            Div("Two"),
            Div("Three"),
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Stack
            from ludic.html import div

            Stack(
                div("One"),
                div("Two"),
                div("Three"),
            )
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("Separating paragraphs in large texts"),
            Item("Creating a list of posts on a blog site"),
            Item("Separating menu and body on a page"),
        ),
        H2("Box"),
        Paragraph(
            "The Box layout adds padding around its content from all "
            "directions. This means that there is an equal amount of space between "
            "the content and the edges of the box, including the left, right, top, "
            "and bottom sides. By default, the Box also includes a border and "
            "a background that is not transparent."
        ),
        H4("Example", anchor=False),
        Box("Box Content Has Padding From All Directions"),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Box

            Box("Content")
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("Creating a page menu or sidebar"),
            Item("Making important text stand out on a page"),
            Item("Using it to highlight a list of actions (buttons)"),
        ),
        H2("Center"),
        Paragraph(
            "The Center layout ensures that its content stays centered on the page. "
            "It sets a maximum width for this content. If the content's width exceeds "
            "this maximum, instead of extending beyond the sides of the page, equal "
            "margins are created on both sides to keep the content centered."
        ),
        H4("Example", anchor=False),
        Center(
            Div("One"),
            Div("Two"),
            Div("Three"),
            style={"max-inline-size": "30ch"},
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Center, Stack
            from ludic.catalog.typography import Paragraph

            Center(
                Stack(
                    Paragraph("Lorem ipsum"),
                    Paragraph("Lorem ipsum"),
                )
            )
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("Main content of a web page"),
            Item("Ideal layout for blog sites"),
        ),
        H2("Cluster"),
        Paragraph(
            "The Cluster layout, when applied, adds margin between all of its inline "
            "children elements. It arranges all of its children elements on a single "
            "line until there is enough space on the page. It's important to note that "
            "the cluster layout is not intended to be used for block-level children "
            "elements like paragraphs."
        ),
        H4("Example", anchor=False),
        Cluster(
            Div("One"),
            Div("Two"),
            Div("Three"),
            Div("Four"),
            Div("Five"),
            Div("Six"),
            Div("Seven"),
            Div("Eight"),
            Div("Nine"),
            Div("Ten"),
            Div("Eleven"),
            Div("Twelve"),
            Div("Thirteen"),
            Div("Fourteen"),
            Div("Fifteen"),
            Div("Sixteen"),
            Div("Seventeen"),
            Div("Eighteen"),
            Div("Nineteen"),
            Div("Twenty"),
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.buttons import Button, ButtonPrimary
            from ludic.catalog.layouts import Cluster

            Cluster(
                Button("Cancel"),
                ButtonPrimary("Save"),
            )
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("Groups of elements that differ in length"),
            Item("Buttons appearing together at the end of a form"),
            Item("A list of tags or keywords"),
        ),
        H2("Sidebar"),
        Paragraph(
            "The Sidebar layout enables you to have two blocks on a page with equal "
            "height but different widths. Typically, the sidebar is narrower than the "
            "main content area. If there isn't enough space to display both the "
            "sidebar and the main content side by side, the layout adjusts into a "
            "stack-like format, where one block is stacked on top of the other."
        ),
        H4("Example", anchor=False),
        WithSidebar(
            Sidebar(
                Div("Menu Item 1"),
                Div("Menu Item 2"),
                Div("Menu Item 3"),
                classes=["showcase"],
            ),
            div(
                Div("One"),
                Div("Two"),
                Div("Three"),
                Div("Four"),
                Div("Five"),
                classes=["showcase"],
            ),
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Box, Sidebar, Stack, WithSidebar
            from ludic.catalog.typography import Paragraph

            WithSidebar(
                Sidebar(
                   div("My Sidebar"),
                ),
                Stack(
                    H1("Content"),
                    Paragraph("Lorem ipsum"),
                ),
            )
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("A page with menu and content"),
            Item("A list of actions next to a form"),
        ),
        H3("Right Sidebar"),
        Paragraph("You can also have the sidebar on the right side instead of left."),
        H4("Example", anchor=False),
        WithSidebar(
            div(
                Div("One"),
                Div("Two"),
                Div("Three"),
                Div("Four"),
                Div("Five"),
                classes=["showcase"],
            ),
            Sidebar(
                Div("Menu Item 1"),
                Div("Menu Item 2"),
                Div("Menu Item 3"),
                classes=["showcase"],
            ),
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Box, Sidebar, Stack, WithSidebar
            from ludic.catalog.typography import Paragraph

            WithSidebar(
                Stack(
                    H1("Content"),
                    Paragraph("Lorem ipsum"),
                ),
                Sidebar(
                   div("My Sidebar"),
                ),
            )
            """,
            language="python",
        ),
        H2("Switcher"),
        Paragraph(
            "The Switcher layout ensures that all of its children elements have the "
            "same width until there is enough space available to display their "
            "content. However, if the layout is placed on a page where there isn't "
            "sufficient room, it collapses and switches to a stack-like format for "
            "display."
        ),
        H4("Example", anchor=False),
        Switcher(
            Div("One"),
            Div("Two"),
            Div("Three"),
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Switcher
            from ludic.html import div

            Switcher(
                div("One"),
                div("Two"),
                div("Three"),
            )
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("Card components advertising products"),
        ),
        H2("Cover"),
        Paragraph(
            "The Cover layout consists of a header, content and footer. The header "
            "is placed above the content and the footer is placed below. The "
            "content is centered both horizontally and vertically."
        ),
        H4("Example", anchor=False),
        Cover(
            Div("Header"),
            div(h1("Title", classes=["text-align-center"]), classes=["cover-main"]),
            Div("Footer"),
            style={"min-block-size": "40vh"},
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Cover

            Cover(
                div("Header"),
                h1("Title"),
                div("Footer"),
            )
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("Introductory page for a website"),
        ),
        H2("Grid"),
        Paragraph(
            "The Grid layout creates a grid of blocks with equal height and width."
        ),
        H4("Example", anchor=False),
        Grid(
            Div("One"),
            Div("Two"),
            Div("Three"),
            Div("Four"),
            Div("Five"),
            Div("Six"),
            Div("Seven"),
            Div("Eight"),
            Div("Nine"),
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Grid

            Grid(
                div("One"),
                div("Two"),
                div("Three"),
                div("Four"),
                div("Five"),
            )
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("Teasers for permalinks or products"),
        ),
        H2("Frame"),
        Paragraph(
            "The Frame layout maintains aspect ratio even if it means the content "
            "needs to be cropped."
        ),
        H4("Example", anchor=False),
        Frame(
            h1("Frame Content"),
            classes=["showcase"],
        ),
        H4("Usage", anchor=False),
        CodeBlock(
            """
            from ludic.catalog.layouts import Frame
            from ludic.html import img

            Frame(
                img(src="/path/to/image", alt="my image"),
            )
            """,
            language="python",
        ),
        H4("Use Cases", anchor=False),
        List(
            Item("cropping media (videos and images) to a desired aspect ratio"),
        ),
        H2("Complex Example"),
        Paragraph(
            "You are free to combine layouts and components together. The "
            "following is an example of a complex layout consisting of multiple "
            "nested layouts mentioned in this tutorial."
        ),
        Cluster(
            ButtonLink(
                "Open Layout In New Tab",
                to=request.url_for("catalog:layout_example"),
                external=True,
                classes=["large", "secondary"],
            ),
            classes=["centered"],
        ),
        Paragraph("Slightly modified code of the layout is shown below."),
        CodeBlock(
            """
            Center(
                Stack(
                    Box(
                        Cluster(
                            b("Inverse Boxed Cluster Menu"),
                            Cluster(
                                Button("Item 1"),
                                ...
                            ),
                            classes=["justify-space-between"],
                        ),
                        classes=["invert"],
                    ),
                    WithSidebar(
                        Stack(
                            H2("Stack", anchor=False),
                            Paragraph(...),
                            H3("Switcher", anchor=False),
                            Switcher(
                                Box("Switcher Item 1"),
                                ...
                            ),
                            H3("Cluster In a Box", anchor=False),
                            Box(
                                Cluster(
                                    ButtonPrimary("Cluster Button 1"),
                                    ...,
                                ),
                            ),
                            H3("Grid Advertisement", anchor=False),
                            Grid(Box(...), ...),
                        ),
                        Sidebar(
                            Box(
                                Stack(
                                    H3("Sidebar", anchor=False),
                                    Button("The Sidebar Item 1"),
                                    ...
                                ),
                            ),
                        ),
                    ),
                    classes=["large"],
                ),
                style={"margin-block": "2rem"},
            )
            """,
            language="python",
        ),
        request=request,
        active_item="layouts",
        title="Ludic - Layouts",
    )


async def layout_example(request: Request) -> BasePage:
    return BasePage(
        Center(
            Stack(
                Box(
                    Cluster(
                        b("Inverse Boxed Cluster Menu"),
                        Cluster(
                            Button("Item 1"),
                            Button("Item 2"),
                            Button("Item 3"),
                            Button("Item 4"),
                        ),
                        classes=["justify-space-between"],
                    ),
                    classes=["invert"],
                ),
                WithSidebar(
                    Stack(
                        H2("Stack", anchor=False),
                        Paragraph(
                            "This is an example paragraph wrapped in a stack. The "
                            "bellow boxes are part of a switcher so they change from "
                            "horizontal layout to a vertical one depending on the "
                            "width of the page. The switcher is part of the content "
                            "of the sidebar layout."
                        ),
                        H3("Switcher", anchor=False),
                        Switcher(
                            Box("Switcher Item 1"),
                            Box("Switcher Item 2"),
                            Box("Switcher Item 3"),
                        ),
                        Paragraph(
                            "On the right side, you have the menu containing a bunch "
                            "of buttons and a header. Bellow, you can see "
                            "a box having a cluster of buttons and a paragraph inside."
                        ),
                        H3("Cluster In a Box", anchor=False),
                        Box(
                            Cluster(
                                ButtonPrimary("Cluster Button 1"),
                                ButtonSuccess("Cluster Button 2"),
                                ButtonInfo("Cluster Button 3"),
                                ButtonDanger("Cluster Button 4"),
                                Paragraph("And some text here..."),
                                Button("Cluster Button 5"),
                            ),
                        ),
                        H3("Grid Advertisement", anchor=False),
                        Grid(
                            Box("This is a grid item advertising this layout."),
                            Box(
                                "The grid creates items of equal size.",
                                classes=["invert"],
                            ),
                            Box("When the page stretches, some items are stacked."),
                            Box(
                                "The switcher is different since it is either "
                                "horizontal or vertical."
                            ),
                            Box(
                                "Grid, on the other hand, can have a configured number "
                                "of items side by side, or stacked, or both.",
                                classes=["invert"],
                            ),
                            Box(
                                "Grid layout always aligns all cells vertically and "
                                "horizontally."
                            ),
                        ),
                    ),
                    Sidebar(
                        Box(
                            Stack(
                                H3("Sidebar", anchor=False),
                                Button("The Sidebar Item 1"),
                                Button("The Sidebar Item 2"),
                                Button("The Sidebar Item 3"),
                            ),
                        ),
                    ),
                ),
                classes=["large"],
            ),
            style={"margin-block": "2rem"},
        ),
        request=request,
    )
