from ludic.catalog.headers import H1, H2
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.web import Request

from web.pages import Page


async def infinite_scroll(request: Request) -> Page:
    return Page(
        H1("Infinite Scroll"),
        Paragraph(
            "The infinite scroll pattern provides a way to load content dynamically"
            "on user scrolling action. This example is almost identical the the "
            f"{Link(
                "Click To Load", to=request.url_for("examples:click_to_load").path)}. "
        ),
        H2("Implementation"),
        Paragraph(
            f"Check the {Link(
                "Click To Load",
                to=request.url_for("examples:click_to_load").path)} example. "
            f"The only difference is the {Code("render()")} implementation with the "
            f"introduction of the {Code("hx_trigger")} and {Code("hx_swap")} "
            "attributes. In the Click To Load example, we used the "
            f"{Code("LoadMoreButton")} to trigger the load action. Here is the "
            f"updated {Code("render()")} method:"
        ),
        CodeBlock(
            """
            @app.endpoint("/contacts/")
            class ContactsSlice(Endpoint[ContactsSliceAttrs]):
                ...

                @override
                def render(self) -> Blank[TableRow]:
                    *init, last = (
                        (contact["id"], contact["name"], contact["email"])
                        for contact in self.attrs["contacts"]
                    )
                    return Blank(
                        *(TableRow(*rows) for rows in init),
                        TableRow(
                            *last,
                            hx_get=self.url_for(ContactsSlice).include_query_params(
                                page=self.attrs["page"] + 1
                            ),
                            hx_trigger="revealed",
                            hx_swap="afterend",
                        ),
                    )
            """,
            language="python",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("infinite_scroll:index")),
        request=request,
        active_item="infinite_scroll",
    )
