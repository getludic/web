from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.quotes import Quote
from ludic.catalog.typography import Code, CodeBlock, Paragraph
from ludic.web import LudicApp, Request
from ludic.web.routing import Mount

from web.examples import bulk_update as bu
from web.examples import click_to_edit as ce
from web.examples import click_to_load as cl
from web.examples import delete_row as dr
from web.examples import edit_row as er
from web.examples import infinite_scroll as isc
from web.examples import lazy_loading as ll
from web.pages import Page

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
async def bulk_update(request: Request) -> Page:
    return Page(
        H1("Bulk Update"),
        Paragraph(
            "This demo shows how to implement a common pattern where rows are "
            "selected and then bulk updated. For the purpose of this example, "
            "we create a table containing people. We also create a column "
            "where we can mark the individual person as active or inactive."
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("bulk-update:index")),
        H2("Implementation"),
        Paragraph(
            "The first thing we need to do is create the table. For this task, we use "
            f"a class-based endpoint called {Code("PeopleTable")} which will contain "
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
            f"Each field in the {Code("PersonAttrs")} definition is marked by the"
            f"{Code("Annotated")} class containing the {Code("ColumnMeta")} "
            "marker. This marker helps generating the table using the "
            f"{Code("create_rows")} function as we'll see bellow."
        ),
        Paragraph(
            "Now we know what kind of data we need to store and what columns to "
            "create. Here is the endpoint implementation rendering the attributes "
            f"as a table as well as handling the {Code("GET")} and {Code("POST")} "
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
                        f"Activated {activations[True]}, "
                        f"deactivated {activations[False]}"
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
                " - handles the POST request which contains form data. Since we "
                f"used the {Code("create_rows")} method, it is possible to use a "
                "parser to automatically convert the form data in a dictionary. "
                "In fact, we are handling a list of people, so we use the "
                f"{Code("ListParser")}. Next, we update our database and return "
                f"the number of activated and deactivated people as a {Code("Toast")} "
                "component that we cover bellow.",
            ),
            Item(
                Code("get"),
                " - handles the GET request which fetches data about people from "
                "the database, creates a list of dicts from that and returns the "
                "table containing these people.",
            ),
            Item(
                Code("render"),
                " - handles rendering of the table. The table is wrapped in a form "
                "so that it is possible to issue a POST request updating the list of "
                "active or inactive people. The form is wrapping the table having the "
                f"columns created according the the {Code("PersonAttrs")} "
                "specification. We also need a button to submit the form and a "
                f"{Code("Toast")} component which displays a message about activated "
                "and deactivated people. The form is submitted via HTMX.",
            ),
        ),
        Paragraph(
            f"Here is the implementation of the {Code("Toast")} component displaying "
            f"the small message next to the {Code("Bulk Update")} button:"
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
        active_item="bulk-update",
    )


@app.get("/click-to-edit")
async def click_to_edit(request: Request) -> Page:
    return Page(
        H1("Click To Edit"),
        Paragraph(
            "The click to edit pattern provides a way to offer inline editing "
            "of all or part of a record without a page refresh. In this example, "
            "we create a customer which we'll be able to edit."
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("click-to-edit:index")),
        H2("Implementation"),
        Paragraph(
            "Before we start implementing the endpoint rendering the HTML form, we "
            "also want to display the data of the customer. The task can be achieved "
            f"by implementing the {Code("Contact")} endpoint which renders the data as "
            "a description list. The endpoint also requires the contact's attributes "
            "which we describe like this:"
        ),
        CodeBlock(
            """
            from typing import Annotated

            from ludic.attrs import Attrs
            from ludic.catalog.forms import FieldMeta

            class ContactAttrs(Attrs):
                id: NotRequired[str]
                first_name: Annotated[str, FieldMeta(label="First Name")]
                last_name: Annotated[str, FieldMeta(label="Last Name")]
                email: Annotated[
                    str, FieldMeta(label="Email", type="email", parser=email_validator)
                ]
            """,
            language="python",
        ),
        Paragraph(
            f"You may have noticed we used the {Code("Annotated")} marker. The reason "
            "for that is that we want to automatically create a form based on this "
            f"specification later. There is also the {Code("email_validator")} parser "
            "which can parse and validate email of the customer. The parser could be "
            "as simple as this:"
        ),
        CodeBlock(
            """
            from ludic.web.parsers import ValidationError

            def email_validator(email: str) -> str:
                if len(email.split("@")) != 2:
                    raise ValidationError("Invalid email")
                return email
            """,
            language="python",
        ),
        Paragraph(
            f"The {Code("contact")} endpoint handles rendering of the customer data "
            f"as well as the {Code("GET")} and {Code("PUT")} HTTP methods:"
        ),
        CodeBlock(
            """
            from typing import Self, override

            from ludic.catalog.forms import Form, create_fields
            from ludic.catalog.layouts import Cluster, Stack
            from ludic.catalog.items import Pairs
            from ludic.web import Endpoint, LudicApp
            from ludic.web.exceptions import NotFoundError
            from ludic.web.parsers import Parser

            from your_app.attrs import ContactAttrs
            from your_app.database import db

            app = LudicApp()

            @app.endpoint("/contacts/{id}")
            class Contact(Endpoint[ContactAttrs]):
                @classmethod
                async def get(cls, id: str) -> Self:
                    contact = db.contacts.get(id)

                    if contact is None:
                        raise NotFoundError("Contact not found")

                    return cls(**contact.dict())

                @classmethod
                async def put(cls, id: str, attrs: Parser[ContactAttrs]) -> Self:
                    contact = db.contacts.get(id)

                    if contact is None:
                        raise NotFoundError("Contact not found")

                    for key, value in attrs.validate().items():
                        setattr(contact, key, value)

                    return cls(**contact.dict())

                @override
                def render(self) -> Stack:
                    return Stack(
                        Pairs(items=self.attrs.items()),
                        Cluster(
                            Button(
                                "Click To Edit",
                                hx_get=self.url_for(ContactForm),
                            ),
                        ),
                        hx_target="this",
                        hx_swap="outerHTML",
                    )
            """,
            language="python",
        ),
        Paragraph("We created a class-based endpoint with the following methods:"),
        List(
            Item(
                Code("get"),
                " - handles the GET request which fetches information about the "
                f"contact from the database, and returns them as the {Code("Contact")} "
                "component to be rendered as HTML.",
            ),
            Item(
                Code("put"),
                " - handles the PUT request which contains form data. Since we "
                f"later use the {Code("create_rows")} method, it is possible to use a "
                "parser to automatically convert the form data into a dictionary. "
                "First, we check that we have the contact in our database, than "
                "we validate the data submitted by the user and update the contact in "
                "our database, and finally, we return the updated contact as the "
                f"{Code("Contact")} component.",
            ),
            Item(
                Code("render"),
                " - handles rendering of the contact data and a button to issue the "
                "HTMX swap operation replacing the content with an editable form.",
            ),
        ),
        Paragraph(f"The last remaining piece is the {Code("ContactForm")} component:"),
        CodeBlock(
            """
            @app.endpoint("/contacts/{id}/form/")
            class ContactForm(Endpoint[ContactAttrs]):
                @classmethod
                async def get(cls, id: str) -> Self:
                    contact = db.contacts.get(id)

                    if contact is None:
                        raise NotFoundError("Contact not found")

                    return cls(**contact.dict())

                @override
                def render(self) -> Form:
                    return Form(
                        *create_fields(self.attrs, spec=ContactAttrs),
                        Cluster(
                            ButtonPrimary("Submit"),
                            ButtonDanger("Cancel", hx_get=self.url_for(Contact)),
                        ),
                        hx_put=self.url_for(Contact),
                        hx_target="this",
                        hx_swap="outerHTML",
                    )
            """,
            language="python",
        ),
        Paragraph("This component only implements two methods:"),
        List(
            Item(
                Code("get"),
                " - handles the GET request which renders the form containing the "
                "contact data stored in the database.",
            ),
            Item(
                Code("render"),
                " - handles rendering of the contact form, a button to submit the "
                "form, and also a button to cancel the edit operation. We use the "
                f"HTMX swap operation to replace the form with the {Code("Contact")} "
                "component on submit or cancel.",
            ),
        ),
        request=request,
        active_item="click-to-edit",
    )


@app.get("/click-to-load")
async def click_to_load(request: Request) -> Page:
    return Page(
        H1("Click To Load"),
        Paragraph(
            "This example shows how to implement click-to-load the next page in "
            "a table of data. We create a table containing a list of contacts "
            "which we lazy load whenever user clicks on a button."
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("click-to-load:index")),
        H2("Implementation"),
        Paragraph(
            "First, we define the contact's attributes and also attributes of an "
            "endpoint-based component we'll use later to hold the contacts and "
            "the current page:"
        ),
        CodeBlock(
            """
            from ludic.attrs import Attrs

            class ContactAttrs(Attrs):
                id: str
                name: str
                email: str

            class ContactsSliceAttrs(Attrs):
                page: int
                contacts: list[ContactAttrs]
            """,
            language="python",
        ),
        Paragraph(
            "Now we need to create two components. First one to display the table "
            "layout and its header columns. The second one to load the contacts data "
            "in the form of the table's rows. The reason for separating these "
            "components is to avoid duplicated code."
        ),
        CodeBlock(
            """
            from typing import Self, override

            from ludic.base import Blank, Component
            from ludic.catalog.tables import Table, TableHead, TableRow
            from ludic.web import Endpoint, LudicApp

            from your_app.attrs import ContactAttrs, ContactsSliceAttrs
            from your_app.database import db
            from your_app.components import LoadMoreButton

            app = LudicApp()

            @app.get("/")
            async def table_of_contacts() -> ContactsTable:
                return ContactsTable(await ContactsSlice.get(QueryParams(page=1))),

            @app.endpoint("/contacts/")
            class ContactsSlice(Endpoint[ContactsSliceAttrs]):
                @classmethod
                async def get(cls, params: QueryParams) -> Self:
                    page = int(params.get("page", 1))
                    return cls(page=page, contacts=db.load_contacts_page(page))

                @override
                def render(self) -> Blank[TableRow]:
                    next_page = self.attrs["page"] + 1
                    return Blank(
                        *(
                            TableRow(contact["id"], contact["name"], contact["email"])
                            for contact in self.attrs["contacts"]
                        ),
                        TableRow(
                            td(
                                LoadMoreButton(
                                    url=self.url_for(
                                        ContactsSlice
                                    ).include_query_params(
                                        page=next_page
                                    ),
                                ),
                                colspan=3,
                            ),
                            id=LoadMoreButton.target,
                        ),
                    )


            class ContactsTable(Component[ContactsSlice, Attrs]):
                @override
                def render(self) -> Table[TableHead, ContactsSlice]:
                    return Table(
                        TableHead("ID", "Name", "Email"),
                        *self.children,
                        classes=["text-align-center"],
                    )
            """,
            language="python",
        ),
        Paragraph(
            "First endpoint is function-based and is rendering the initial table "
            f"of contacts. We use the {Code("ContactsSlice.get()")} method to load "
            "the first page. It would probably be better to separate this loading "
            "to some handler function."
        ),
        Paragraph(
            f"The {Code("ContactsSlice")} endpoint-based component is loading the "
            "table rows and implements two methods:"
        ),
        List(
            Item(
                Code("get"),
                " - handles the GET request which loads contacts from the database. "
                "The handler returns an instance of itself.",
            ),
            Item(
                Code("render"),
                f" - handles rendering of the table rows and the {Code("Load More")} "
                "button. In order for everything to work properly, we render only "
                f"the table's rows while wrapping them in the {Code("Blank")} "
                "component. This component does not render any HTML element, it's just "
                "a wrapper when we want to render a list of elements.",
            ),
        ),
        Paragraph(
            f"Last, the {Code("ContactsTable")} class is a regular component that "
            "renders the table's columns."
        ),
        Paragraph(
            f"The last remaining piece is the {Code("LoadMoreButton")} component which "
            f"triggers the {Code("GET")} request calling the {Code("ContactsSlice")} "
            "method to load more contact data:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import Attrs
            from ludic.base import ComponentStrict
            from ludic.catalog.buttons import ButtonPrimary

            class LoadMoreAttrs(Attrs):
                url: str

            class LoadMoreButton(ComponentStrict[LoadMoreAttrs]):
                target: str = "replace-me"

                @override
                def render(self) -> ButtonPrimary:
                    return ButtonPrimary(
                        "Load More Agents...",
                        hx_get=self.attrs["url"],
                        hx_target=f"#{self.target}",
                        hx_swap="outerHTML",
                    )
            """,
            language="python",
        ),
        Paragraph(
            "We use the HTMX swap operation to replace the button itself with a new "
            f"slice of contacts rendered by the {Code("ContactsSlice")} endpoint. "
            "That is, the next page of rows as well as the button itself running the "
            f"HTMX operation. Since the {Code("ContactsSlice")} always bumps the "
            "button link's page, we get the next page of contacts on every click."
        ),
        request=request,
        active_item="click-to-load",
    )


@app.get("/delete-row")
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
        LazyLoader(load_url=request.url_for("delete-row:index")),
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
        active_item="delete-row",
    )


@app.get("/edit-row")
async def edit_row(request: Request) -> Page:
    return Page(
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
async def infinite_scroll(request: Request) -> Page:
    return Page(
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
async def lazy_loading(request: Request) -> Page:
    return Page(
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
