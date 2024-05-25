from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.typography import Code, CodeBlock, Paragraph
from ludic.web import Request

from web.pages import Page


def delete_row(request: Request) -> Page:
    return Page(
        H1("Delete Row"),
        Paragraph(
            "This example shows how to implement a delete button that removes "
            "a table row upon completion. For this example, we use have a sample "
            "database of people which we display in a table. Each row in the table "
            "can be deleted by clicking a button and a confirmation prompt."
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("delete_row:index")),
        H2("Implementation"),
        Paragraph(
            "Since we want to display people as rows in a table, we can create a "
            "dedicated class-based endpoint which can render itself like a component. "
            "Before we do that, we also need to declare what kind of data this "
            "endpoint handles:"
        ),
        CodeBlock(
            """
            from ludic.attrs import Attrs

            class PersonAttrs(Attrs):
                id: str
                name: str
                email: str
                active: bool

            class PeopleAttrs(Attrs):
                people: list[PersonAttrs]
            """,
            language="python",
        ),
        Paragraph("Now we can use these attributes in our class-based endpoint:"),
        CodeBlock(
            """
            from typing import override

            from ludic.base import Component
            from ludic.catalog.tables import Table, TableRow
            from ludic.catalog.buttons import ButtonDanger
            from ludic.web import Endpoint, LudicApp

            from your_app.attrs import PersonAttrs
            from your_app.database import db

            app = LudicApp()

            @app.endpoint("/people/{id}")
            class PersonRow(Endpoint[PersonAttrs]):
                @classmethod
                def delete(cls, id: str) -> None:
                    try:
                        db.people.pop(id)
                    except KeyError:
                        raise NotFoundError("Person not found")

                @override
                def render(self) -> TableRow:
                    return TableRow(
                        self.attrs["name"],
                        self.attrs["email"],
                        "Active" if self.attrs["active"] else "Inactive",
                        ButtonDanger(
                            "Delete",
                            hx_delete=self.url_for(PersonRow),
                            classes=["small"]
                        ),
                    )
            """,
            language="python",
        ),
        Paragraph("We created a class-based endpoint with the following methods:"),
        List(
            Item(
                Code("delete"),
                " - handles the DELETE request which removes a person from the "
                "database. We don't need to return anything in this case.",
            ),
            Item(
                Code("render"),
                " - handles rendering of the table. Apart from the textual columns, "
                "we also render an action button to delete a row which is hooked to "
                f"the {Code("PersonRow.delete()")} method.",
            ),
        ),
        Paragraph(
            "The last remaining part is the table with people itself. We can create "
            "another class-based endpoint for this task:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.base import Component
            from ludic.catalog.tables import Table, TableRow
            from ludic.catalog.buttons import ButtonDanger
            from ludic.web import Endpoint, LudicApp

            from your_app.attrs import PeopleAttrs
            from your_app.database import db

            # ... the PersonRow class is omitted here

            @app.endpoint("/people/")
            class PeopleTable(Endpoint[PeopleAttrs]):
                styles = {
                    "tr.htmx-swapping td": {
                        "opacity": "0",
                        "transition": "opacity 1s ease-out",
                    }
                }

                @classmethod
                def get(cls) -> Self:
                    return cls(people=[person.dict() for person in db.people.values()])

                @override
                def render(self) -> Table[TableHead, PersonRow]:
                    return Table(
                        TableHead("Name", "Email", "Active", ""),
                        *(PersonRow(**person) for person in self.attrs["people"]),
                        body_attrs=HtmxAttrs(
                            hx_confirm="Are you sure?",
                            hx_target="closest tr",
                            hx_swap="outerHTML swap:1s",
                        ),
                        classes=["text-align-center"],
                    )
            """,
            language="python",
        ),
        Paragraph("We created a class-based endpoint with the following methods:"),
        List(
            Item(
                Code("get"),
                " - handles the GET request which returns an instance of the "
                f"{Code("PeopleTable")} filled with a list of people fetched "
                "from database.",
            ),
            Item(
                Code("render"),
                " - handles rendering of the table of people. We use a special "
                f"{Code("body_attrs")} attribute to configure HTMX operations on "
                f"the {Code("tbody")} element.",
            ),
        ),
        request=request,
        active_item="delete_row",
        title="Ludic - Delete Row",
    )
