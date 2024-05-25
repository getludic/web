from ludic.catalog.headers import H1, H4
from ludic.catalog.loaders import Loading
from ludic.catalog.typography import CodeBlock, Paragraph
from ludic.web import Request

from web.pages import Page


def loaders(request: Request) -> Page:
    return Page(
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
        title="Ludic - Loaders",
    )
