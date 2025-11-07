from ludic.catalog.headers import H1
from ludic.catalog.messages import (
    Message,
    MessageDanger,
    MessageInfo,
    MessageSuccess,
    MessageWarning,
    Title,
)
from ludic.catalog.typography import Code, CodeBlock, Paragraph
from ludic.web import Request

from web.pages import Page


def messages(request: Request) -> Page:
    return Page(
        H1("Messages"),
        Paragraph(
            f"The module {Code('ludic.catalog.messages')} contains the following "
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
                Message,
                MessageSuccess,
                MessageInfo,
                MessageWarning,
                MessageDanger,
                Title
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
            f"Note that you don't need to specify the {Code('Title')} component. "
            "Here is how the message renders without the title:"
        ),
        Message(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        ),
        request=request,
        active_item="messages",
        title="Ludic - Messages",
    )
