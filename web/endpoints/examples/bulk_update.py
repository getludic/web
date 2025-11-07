from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.web import Request

from web import config
from web.pages import Page


async def bulk_update(request: Request) -> Page:
    return Page(
        H1("Bulk Update"),
        Paragraph(
            "This demo shows how to implement a common pattern where rows are "
            "selected and then bulk updated. For the purpose of this example, "
            "we create a table containing people. We also create a column "
            "where we can mark the individual person as active or inactive."
        ),
        List(
            Item(
                Link(
                    "Full Code at GitHub",
                    to=f"{config.GITHUB_REPO_URL}/blob/main/examples/bulk_update.py",
                )
            ),
            Item(
                Link("Source at htmx.org", to="https://htmx.org/examples/bulk-update/")
            ),
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("bulk_update:index")),
        H2("Implementation"),
        Paragraph(
            "The first thing we need to do is create the table. For this task, we use "
            f"a class-based endpoint called {Code('PeopleTable')} which will contain "
            "the list of people. This list of people is going to be the endpoint's "
            "attributes, so we create them first:"
        ),
        CodeBlock(
            """
            from typing import Annotated

            from ludic.attrs import Attrs
            from ludic.catalog.forms import FieldMeta
            from ludic.catalog.tables import ColumnMeta

            class PersonAttrs(Attrs, total=False):
                id: Annotated[str, ColumnMeta(identifier=True)]
                name: Annotated[str, ColumnMeta()]
                email: Annotated[str, ColumnMeta()]
                active: Annotated[
                    bool,
                    ColumnMeta(kind=FieldMeta(kind="checkbox", label=None)),
                ]

            class PeopleAttrs(Attrs):
                people: list[PersonAttrs]
            """,
            language="python",
        ),
        Paragraph(
            f"Each field in the {Code('PersonAttrs')} definition is marked by the"
            f"{Code('Annotated')} class containing the {Code('ColumnMeta')} "
            "marker. This marker helps generating the table using the "
            f"{Code('create_rows')} function as we'll see bellow."
        ),
        Paragraph(
            "Now we know what kind of data we need to store and what columns to "
            "create. Here is the endpoint implementation rendering the attributes "
            f"as a table as well as handling the {Code('GET')} and {Code('POST')} "
            "HTTP methods:"
        ),
        CodeBlock(
            """
            from typing import Self, override

            from ludic.catalog.layouts import Cluster
            from ludic.catalog.tables import Table, create_rows
            from ludic.catalog.forms import Form
            from ludic.web import Endpoint, LudicApp
            from ludic.web.exceptions import NotFoundError
            from ludic.web.parsers import ListParser

            from your_app.attrs import PeopleAttrs, PersonAttrs
            from your_app.components import Toast
            from your_app.database import db

            app = LudicApp()

            @app.endpoint("/people/")
            class PeopleTable(Endpoint[PeopleAttrs]):
                @classmethod
                async def post(cls, data: ListParser[PersonAttrs]) -> Toast:
                    items = {row["id"]: row for row in data.validate()}
                    activations = {True: 0, False: 0}

                    for person in db.people.values():
                        active = items.get(person.id, {}).get("active", False)
                        if person.active != active:
                            person.active = active
                            activations[active] += 1

                    return Toast(
                        t"Activated {activations[True]}, "
                        t"deactivated {activations[False]}"
                    )

                @classmethod
                async def get(cls) -> Self:
                    return cls(people=[person.dict() for person in db.people.values()])

                @override
                def render(self) -> Form:
                    return Form(
                        Table(*create_rows(self.attrs["people"], spec=PersonAttrs)),
                        Cluster(
                            ButtonPrimary("Bulk Update", type="submit"),
                            Toast(),
                        ),
                        hx_post=self.url_for(PeopleTable),
                        hx_target=Toast.target,
                        hx_swap="outerHTML settle:3s",
                    )
            """,
            language="python",
        ),
        Paragraph("We created a class-based endpoint with the following methods:"),
        List(
            Item(
                Code("post"),
                " – handles the POST request which contains form data. Since we "
                f"used the {Code('create_rows')} method, it is possible to use a "
                "parser to automatically convert the form data in a dictionary. "
                "In fact, we are handling a list of people, so we use the "
                f"{Code('ListParser')}. Next, we update our database and return "
                f"the number of activated and deactivated people as a {Code('Toast')} "
                "component that we cover bellow.",
            ),
            Item(
                Code("get"),
                " – handles the GET request which fetches data about people from "
                "the database, creates a list of dicts from that and returns the "
                "table containing these people.",
            ),
            Item(
                Code("render"),
                " – handles rendering of the table. The table is wrapped in a form "
                "so that it is possible to issue a POST request updating the list of "
                "active or inactive people. The form is wrapping the table having the "
                f"columns created according the the {Code('PersonAttrs')} "
                "specification. We also need a button to submit the form and a "
                f"{Code('Toast')} component which displays a message about activated "
                "and deactivated people. The form is submitted via HTMX.",
            ),
        ),
        Paragraph(
            f"Here is the implementation of the {Code('Toast')} component displaying "
            f"the small message next to the {Code('Bulk Update')} button:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.html import span, style

            class Toast(span):
                id: str = "toast"
                target: str = f"#{id}"
                styles = style.use(
                    lambda theme: {
                        Toast.target: {
                            "background": theme.colors.success,
                            "padding": f"{theme.sizes.xxxxs} {theme.sizes.xxxs}",
                            "font-size": theme.fonts.size * 0.9,
                            "border-radius": "3px",
                            "opacity": "0",
                            "transition": "opacity 3s ease-out",
                        },
                        f"{Toast.target}.htmx-settling": {
                            "opacity": "100",
                        },
                    }
                )

                @override
                def render(self) -> span:
                    return span(*self.children, id=self.id)
            """,
            language="python",
        ),
        request=request,
        active_item="bulk_update",
        title="Ludic - Bulk Update",
    )
