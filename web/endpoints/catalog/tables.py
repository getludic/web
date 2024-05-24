from typing import Annotated

from ludic.attrs import Attrs
from ludic.catalog.forms import FieldMeta, Form
from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.tables import ColumnMeta, Table, TableHead, TableRow, create_rows
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.web import Request

from web.pages import Page


class SamplePersonAttrs(Attrs):
    id: Annotated[int, ColumnMeta(label="ID")]
    name: Annotated[str, ColumnMeta(label="Full Name")]
    email: Annotated[str, ColumnMeta(label="Email")]


class SampleContactAttrs(Attrs):
    id: Annotated[int, ColumnMeta(identifier=True)]
    name: Annotated[str, ColumnMeta(label="Full Name")]
    email: Annotated[str, ColumnMeta(label="Email")]
    active: Annotated[
        bool, ColumnMeta(label="Active", kind=FieldMeta(kind="checkbox", label=None))
    ]


def tables(request: Request) -> Page:
    people_attrs_list: list[SamplePersonAttrs] = [
        {"id": 1, "name": "John Doe", "email": "john@j.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@s.com"},
    ]
    contacts_attrs_list: list[SampleContactAttrs] = [
        {"id": 1, "name": "John Doe", "email": "john@j.com", "active": True},
        {"id": 2, "name": "Jane Smith", "email": "jane@s.com", "active": False},
    ]

    return Page(
        H1("Tables"),
        Paragraph(
            f"These components located in {Code("ludic.catalog.tables")} are in an "
            "experimental mode. There is the possibility to automatically create "
            "tables even containing form fields and actions from annotations, but "
            "it is far from production-ready."
        ),
        H2("Creating a Table"),
        Paragraph(
            f"The {Code("Table")} component accepts a {Code("TableHead")} as the first "
            f"item and any number of {Code("TableRow")} items."
        ),
        Table(
            TableHead("First Name", "Last Name", "Age"),
            TableRow("John", "Doe", 42),
            TableRow("Jane", "Smith", 23),
            classes=["text-align-center"],
        ),
        CodeBlock(
            """
            from ludic.catalog.tables import Table, TableHead, TableRow

            Table(
                TableHead("First Name", "Last Name","Age"),
                TableRow("John", "Doe", 42),
                TableRow("Jane", "Smith", 23),
                classes=["text-align-center"],
            )
            """,
            language="python",
        ),
        Paragraph(
            "You can also specify different types of header and body. It might happen "
            "that you created your own component representing the table head and body:"
        ),
        CodeBlock(
            """
            from ludic.catalog.tables import Table

            from your_app.components import PersonHead, PersonRow

            Table[PersonHead, PersonRow](
                PersonHead("Name", "Age"),
                PersonRow("John", 42),
                PersonRow("Jane", 23),
            )
            """,
            language="python",
        ),
        Paragraph(
            "Note that the type specification in the square brackets is only for the "
            "type-checkers to pass."
        ),
        H2("Generating Table Rows"),
        Paragraph(
            f"The {Code("create_rows")} function can be used to generate rows in the "
            "table based on given specification. Here is an example:"
        ),
        CodeBlock(
            """
            from typing import Annotated

            from ludic.catalog.tables import ColumnMeta, Table, create_rows
            from ludic.types import Attrs

            class PersonAttrs(Attrs):
                id: Annotated[int, ColumnMeta(label="ID")]
                name: Annotated[str, ColumnMeta(label="Full Name")]
                email: Annotated[str, ColumnMeta(label="Email")]

            people: list[PersonAttrs] = [
                {"id": 1, "name": "John Doe", "email": "john@j.com"},
                {"id": 2, "name": "Jane Smith", "email": "jane@s.com"},
            ]

            rows = create_rows(people, spec=PersonAttrs)
            table = Table(*rows)
            """,
            language="python",
        ),
        Paragraph("This would render the following table:"),
        Table(
            *create_rows(people_attrs_list, spec=SamplePersonAttrs),
            classes=["text-align-center"],
        ),
        H3("Table With Form Fields"),
        Paragraph(
            "There is also an experimental support for tables containing form fields."
            "The way it works is that you wrap your table in a form and use the "
            f"{Code("create_rows")} function to generate the rows. Here is an example:"
        ),
        Form(
            Table(*create_rows(contacts_attrs_list, spec=SampleContactAttrs)),
            classes=["text-align-center"],
        ),
        CodeBlock(
            """
            from typing import Annotated

            from ludic.catalog.tables import ColumnMeta, Table, create_rows
            from ludic.types import Attrs

            class ContactAttrs(Attrs):
                id: Annotated[int, ColumnMeta(identifier=True)]
                name: Annotated[str, ColumnMeta(label="Full Name")]
                email: Annotated[str, ColumnMeta(label="Email")]
                active: Annotated[
                    bool,
                    ColumnMeta(
                        label="Active", kind=FieldMeta(kind="checkbox", label=None)
                    )
                ]

            contacts: list[ContactAttrs] = [
                {"id": 1, "name": "John Doe", "email": "john@j.com", "active": True},
                {"id": 2, "name": "Jane Smith", "email": "jane@s.com", "active": False},
            ]

            rows = create_rows(contacts, spec=ContactAttrs)
            table = Table(*rows)
            """,
            language="python",
        ),
        Paragraph(
            "The role of the identifier column is to be able to parse the form data "
            f"using the {Code("ListParser")} function as documented in the {Link(
                "Parsers section",
                to=f"{request.url_for("docs:web_framework").path}#parsing-collections"
            )} of the documentation."
        ),
        request=request,
        active_item="tables",
    )
