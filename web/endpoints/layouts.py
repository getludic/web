from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.layouts import (
    Box,
    Center,
    Cluster,
    Sidebar,
    Stack,
    Switcher,
    WithSidebar,
)
from ludic.catalog.lists import Item, List
from ludic.catalog.messages import Message, Title
from ludic.catalog.typography import Code, Link, Paragraph
from ludic.html import div
from ludic.web import LudicApp, Request

from web.components import Div
from web.pages import PageWithMenu

app = LudicApp()


@app.get("/layouts/")
def layouts(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Layouts"),
        Paragraph(
            "Layouts create a flexible structure for your user interface. "
            "The layouts in this module are based on the Every Layout Book. "
            "If you haven't read the book, go read it now: "
        ),
        List(Item(Link("Every Layout Book", to="https://every-layout.dev/"))),
        Paragraph(
            "These layouts allow us to create complex user interfaces with "
            "minimal CSS which are responsive and readable on all devices. "
            "The layouts can be combined together."
        ),
        Paragraph(
            f"All layouts are located in the {Code("ludic.catalog.layouts")} " "module."
        ),
        Message(
            Title("Viewing this page on mobile devices"),
            "If you are viewing this page on mobile devices, you won't probably see "
            "the layouts examples correctly rendered. You can always switch between "
            "desktop mode and mobile if you want to see the difference in rendering.",
        ),
        H2("Stack"),
        Stack(
            Div("One"),
            Div("Two"),
            Div("Three"),
        ),
        H2("Box"),
        Box(
            "Box Content Has Padding From All Directions",
            classes=["transparent", "showcase"],
        ),
        H2("Center"),
        Center(
            Div("One"),
            Div("Two"),
            Div("Three"),
            style={"max-inline-size": "30ch"},
        ),
        H2("Cluster"),
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
        H2("Sidebar"),
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
        H3("Right Sidebar"),
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
        H2("Switcher"),
        Switcher(
            Div("One"),
            Div("Two"),
            Div("Three"),
        ),
        request=request,
        active_item="layouts",
    )
