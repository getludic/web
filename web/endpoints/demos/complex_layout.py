from ludic.catalog.buttons import (
    Button,
    ButtonDanger,
    ButtonInfo,
    ButtonPrimary,
    ButtonSuccess,
)
from ludic.catalog.headers import H2, H3
from ludic.catalog.layouts import (
    Box,
    Center,
    Cluster,
    Grid,
    Sidebar,
    Stack,
    Switcher,
    WithSidebar,
)
from ludic.catalog.typography import Paragraph
from ludic.html import b
from ludic.web import LudicApp, Request

from web.pages import BasePage

app = LudicApp()


@app.get("/")
async def index(request: Request) -> BasePage:
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
