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
from ludic.catalog.headers import H1, H2
from ludic.catalog.layouts import Box, Cluster
from ludic.catalog.typography import Code, CodeBlock, Paragraph
from ludic.web import Request

from web.pages import Page


def buttons(request: Request) -> Page:
    return Page(
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
                ButtonLink("ButtonLink", to="#"),
                classes=["centered"],
            ),
        ),
        CodeBlock(
            """
            from ludic.catalog.buttons import (
                Button,
                ButtonPrimary,
                ButtonSecondary,
                ButtonSuccess,
                ButtonInfo,
                ButtonWarning,
                ButtonDanger,
                ButtonLink
            )

            Button("Button")
            ButtonPrimary("ButtonPrimary")
            ButtonSecondary("ButtonSecondary")
            ButtonSuccess("ButtonSuccess")
            ButtonInfo("ButtonInfo")
            ButtonWarning("ButtonWarning")
            ButtonDanger("ButtonDanger")
            ButtonLink("ButtonLink", to="/")
            """,
            language="python",
        ),
        Paragraph(
            f"The {Code("ButtonLink")} component can be styled like any other "
            f"button using the {Code("classes")} attribute:"
        ),
        CodeBlock(
            """
            from ludic.catalog.buttons import ButtonLink

            ButtonLink("ButtonLink", to="/", classes=["warning"])
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
