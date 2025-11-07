from ludic.catalog.buttons import ButtonLink
from ludic.catalog.headers import H2
from ludic.catalog.layouts import Cluster
from ludic.catalog.typography import CodeBlock, Link, Paragraph
from ludic.web import Request

from web.pages import Page


def complex_layout(request: Request) -> Page:
    return Page(
        H2("Layout Example"),
        Paragraph(
            "You are free to combine layouts and components together as described in "
            f"the {Link('Layouts', to=request.url_for('catalog:layouts').path)} "
            "section. The following is an example of a more complex layout consisting "
            "of multiple nested components using CSS utilities to tweak final design."
        ),
        Cluster(
            ButtonLink(
                "Open Layout In New Tab",
                to=str(request.url_for("complex_layout:index")),
                external=True,
                classes=["large", "secondary"],
            ),
            classes=["centered"],
        ),
        Paragraph("Slightly modified code of the layout is shown below."),
        CodeBlock(
            """
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
        active_item="complex_layout",
        title="Ludic - Complex Layout",
    )
