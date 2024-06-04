from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.web import Request

from web import config
from web.pages import Page


async def lazy_loading(request: Request) -> Page:
    return Page(
        H1("Lazy Loading"),
        Paragraph(
            "This example shows how to lazily load an element on a page. This "
            "lazy loading can be used for loading large images."
        ),
        List(
            Item(
                Link(
                    "Full Code at GitHub",
                    to=f"{config.GITHUB_REPO_URL}/blob/main/examples/lazy_loading.py",
                )
            ),
            Item(Link("Source at htmx.org", to="https://htmx.org/examples/lazy-load/")),
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("lazy_loading:index")),
        H2("Implementation"),
        Paragraph(
            "The lazy loading functionality is super simple to implement "
            "in Ludic. You can create just two function-based endpoints "
            f"and use the {Code("LazyLoader")} component from the catalog: "
        ),
        CodeBlock(
            """
            from ludic.catalog.headers import H3
            from ludic.catalog.layouts import Box, Frame
            from ludic.catalog.loaders import LazyLoader
            from ludic.web import LudicApp, Request

            app = LudicApp()

            @app.get("/")
            async def index(request: Request) -> LazyLoader:
                return LazyLoader(load_url=request.url_for(load_content))

            @app.get("/load/")
            async def load_content() -> Box:
                return Box(
                    Frame(
                        H3("Content Loaded"),
                    )
                )
            """,
            language="python",
        ),
        request=request,
        active_item="lazy_loading",
        title="Ludic - Lazy Loading",
    )
