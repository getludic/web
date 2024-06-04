from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.web import Request

from web import config
from web.pages import Page


async def edit_row(request: Request) -> Page:
    return Page(
        H1("Edit Row"),
        Paragraph(
            "This example shows how to implement editable rows. In this example, we "
            "create a table with a row for each person in the database. Each row "
            "contains an edit button which allows inline editing of user's data."
        ),
        List(
            Item(
                Link(
                    "Full Code at GitHub",
                    to=f"{config.GITHUB_REPO_URL}/blob/main/examples/edit_row.py",
                )
            ),
            Item(Link("Source at htmx.org", to="https://htmx.org/examples/edit-row/")),
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("edit_row:index")),
        H2("Implementation"),
        Paragraph("In this example, we'll be creating three class-based endpoints:"),
        NumberedList(
            Item(
                "One for displaying the person's information in a row with the "
                "edit button;"
            ),
            Item(
                "Another for displaying the form for editing the person's data and "
                "an action button to confirm the changes;"
            ),
            Item("Last one for displaying the whole table of people."),
        ),
        Paragraph(
            "First, we create the attributes which define what kind of data "
            "we want to display:"
        ),
        CodeBlock(
            """
            from typing import Annotated, NotRequired

            from ludic.attrs import Attrs
            from ludic.catalog.tables import ColumnMeta

            class PersonAttrs(Attrs):
                id: NotRequired[str]
                name: Annotated[str, ColumnMeta()]
                email: Annotated[str, ColumnMeta()]

            class PeopleAttrs(Attrs):
                people: list[PersonAttrs]
            """,
            language="python",
        ),
        Paragraph(
            f"Now we create the {Code("PersonRow")} endpoint for displaying the "
            "person's information in a row:"
        ),
        CodeBlock(
            """
            from typing import Self, override

            from ludic.base import JavaScript
            from ludic.catalog.buttons import ButtonPrimary
            from ludic.catalog.tables import TableRow
            from ludic.web import Endpoint, LudicApp
            from ludic.web.parsers import Parser

            from your_app.attrs import PersonAttrs
            from your_app.database import db

            app = LudicApp()

            @app.endpoint("/people/{id}")
            class PersonRow(Endpoint[PersonAttrs]):
                on_click_script: JavaScript = JavaScript(
                    \"\"\"
                    let editing = document.querySelector('.editing')

                    if (editing) {
                        alert('You are already editing a row')
                    } else {
                        htmx.trigger(this, 'edit')
                    }
                    \"\"\"
                )

                @classmethod
                async def put(cls, id: str, data: Parser[PersonAttrs]) -> Self:
                    person = db.people.get(id)

                    if person is None:
                        raise NotFoundError("Person not found")

                    for attr, value in data.validate().items():
                        setattr(person, attr, value)

                    return cls(**person.dict())

                @classmethod
                async def get(cls, id: str) -> Self:
                    person = db.people.get(id)

                    if person is None:
                        raise NotFoundError("Person not found")

                    return cls(**person.dict())

                @override
                def render(self) -> TableRow:
                    return TableRow(
                        self.attrs["name"],
                        self.attrs["email"],
                        ButtonPrimary(
                            "Edit",
                            hx_get=self.url_for(PersonForm),
                            hx_trigger="edit",
                            on_click=self.on_click_script,
                            classes=["small"],
                        ),
                    )
            """,
            language="python",
        ),
        Paragraph(
            "We created a class-based endpoint, here is the explanation of "
            "its individual parts:"
        ),
        List(
            Item(
                Code("on_click_script"),
                " - this script is executed when the edit button is clicked. We "
                "don't want to allow the user to edit multiple rows at once so we "
                "check if the user is already editing a row.",
            ),
            Item(
                Code("put"),
                " - handles the PUT request which updates a person in the "
                "database. We return the updated person data as a row in the response.",
            ),
            Item(
                Code("get"),
                " - handles the GET request which returns an instance of the "
                f"{Code("PeopleRow")} of the requested person.",
            ),
            Item(
                Code("render"),
                " - handles rendering of the row. Apart from the textual columns, "
                "we also render an action button to edit a row.",
            ),
        ),
        Paragraph(
            "Now, we want to create an endpoint which renders the form we want to "
            "display when a row is being edited:"
        ),
        CodeBlock(
            """
            from typing import Self, override

            from ludic.catalog.buttons import ButtonSecondary, ButtonSuccess
            from ludic.catalog.forms import InputField
            from ludic.catalog.tables import TableRow
            from ludic.web import Endpoint

            from your_app.attrs import PersonAttrs
            from your_app.database import db

            @app.endpoint("/people/{id}/form/")
            class PersonForm(Endpoint[PersonAttrs]):
                @classmethod
                async def get(cls, id: str) -> Self:
                    person = db.people.get(id)

                    if person is None:
                        raise NotFoundError("Person not found")

                    return cls(**person.dict())

                @override
                def render(self) -> TableRow:
                    return TableRow(
                        InputField(name="name", value=self.attrs["name"]),
                        InputField(name="email", value=self.attrs["email"]),
                        Cluster(
                            ButtonSecondary(
                                "Cancel",
                                hx_get=self.url_for(PersonRow),
                                classes=["small"],
                            ),
                            ButtonSuccess(
                                "Save",
                                hx_put=self.url_for(PersonRow),
                                hx_include="closest tr",
                                classes=["small"],
                            ),
                            classes=["cluster-small"],
                        ),
                        classes=["editing"],
                    )
            """,
            language="python",
        ),
        Paragraph("We created a class-based endpoint with the following methods:"),
        List(
            Item(
                Code("get"),
                " - handles the GET request which renders the requested person's row.",
            ),
            Item(
                Code("render"),
                " - handles rendering of the person's edit row. Apart from the name "
                "and email columns, we are also rendering two action buttons, one "
                "canceling the action and one saving the changes.",
            ),
        ),
        Paragraph(
            "The last class-based endpoint is for displaying the table of people:"
        ),
        CodeBlock(
            """
            from typing import Self, override

            from ludic.catalog.tables import Table, TableHead
            from ludic.web import Endpoint

            from your_app.attrs import PeopleAttrs
            from your_app.database import db

            # ... PersonRow and PersonForm classes omitted along with the imports

            @app.endpoint("/people/")
            class PeopleTable(Endpoint[PeopleAttrs]):
                @classmethod
                async def get(cls) -> Self:
                    return cls(people=[person.dict() for person in db.people.values()])

                @override
                def render(self) -> Table[TableHead, PersonRow]:
                    return Table[TableHead, PersonRow](
                        TableHead("Name", "Email", "Action"),
                        *(PersonRow(**person) for person in self.attrs["people"]),
                        body_attrs=HtmxAttrs(
                            hx_target="closest tr"
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
        active_item="edit_row",
        title="Ludic - Edit Row",
    )
