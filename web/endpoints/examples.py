from ludic.catalog.headers import H1, H2
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.quotes import Quote
from ludic.web import LudicApp, Request
from ludic.web.routing import Mount

from web.examples import bulk_update as bu
from web.examples import click_to_edit as ce
from web.examples import click_to_load as cl
from web.examples import delete_row as dr
from web.examples import edit_row as er
from web.examples import infinite_scroll as isc
from web.examples import lazy_loading as ll
from web.pages import PageWithMenu

app = LudicApp(
    routes=[
        Mount("/examples/bulk-update/", bu.app, name="bulk-update"),
        Mount("/examples/click-to-edit/", ce.app, name="click-to-edit"),
        Mount("/examples/click-to-load/", cl.app, name="click-to-load"),
        Mount("/examples/delete-row/", dr.app, name="delete-row"),
        Mount("/examples/edit-row/", er.app, name="edit-row"),
        Mount("/examples/infinite-scroll/", isc.app, name="infinite-scroll"),
        Mount("/examples/lazy-loading/", ll.app, name="lazy-loading"),
    ],
)


@app.get("/bulk-update")
async def bulk_update(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Bulk Update"),
        Quote(
            "This demo shows how to implement a common pattern where rows are "
            "selected and then bulk updated.",
            source_url="https://htmx.org/examples/bulk-update/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("bulk-update:index")),
        request=request,
        active_item="bulk-update",
    )


@app.get("/click-to-edit")
async def click_to_edit(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Click To Edit"),
        Quote(
            "The click to edit pattern provides a way to offer inline editing "
            "of all or part of a record without a page refresh.",
            source_url="https://htmx.org/examples/click-to-edit/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("click-to-edit:index")),
        request=request,
        active_item="click-to-edit",
    )


@app.get("/click-to-load")
async def click_to_load(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Click To Load"),
        Quote(
            "This example shows how to implement click-to-load the next page in "
            "a table of data.",
            source_url="https://htmx.org/examples/click-to-load/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("click-to-load:index")),
        request=request,
        active_item="click-to-load",
    )


@app.get("/delete-row")
def delete_row(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Delete Row"),
        Quote(
            "This example shows how to implement a delete button that removes "
            "a table row upon completion.",
            source_url="https://htmx.org/examples/delete-row/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("delete-row:index")),
        request=request,
        active_item="delete-row",
    )


@app.get("/edit-row")
async def edit_row(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Edit Row"),
        Quote(
            "This example shows how to implement editable rows.",
            source_url="https://htmx.org/examples/edit-row/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("edit-row:index")),
        request=request,
        active_item="edit-row",
    )


@app.get("/infinite-scroll")
async def infinite_scroll(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Infinite Scroll"),
        Quote(
            "The infinite scroll pattern provides a way to load content dynamically"
            "on user scrolling action.",
            source_url="https://htmx.org/examples/infinite-scroll/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("infinite-scroll:index")),
        request=request,
        active_item="infinite-scroll",
    )


@app.get("/lazy-loading")
async def lazy_loading(request: Request) -> PageWithMenu:
    return PageWithMenu(
        H1("Lazy Loading"),
        Quote(
            "This example shows how to lazily load an element on a page.",
            source_url="https://htmx.org/examples/lazy-load/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("lazy-loading:index")),
        request=request,
        active_item="lazy-loading",
    )
