from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.web import Request

from web import config
from web.pages import Page


async def click_to_load(request: Request) -> Page:
    return Page(
        H1("Click To Load"),
        Paragraph(
            "This example shows how to implement click-to-load the next page in "
            "a table of data. We create a table containing a list of contacts "
            "which we lazy load whenever user clicks on a button."
        ),
        List(
            Item(
                Link(
                    "Full Code at GitHub",
                    to=f"{config.GITHUB_REPO_URL}/blob/main/examples/click_to_load.py",
                )
            ),
            Item(
                Link(
                    "Source at htmx.org", to="https://htmx.org/examples/click-to-load/"
                )
            ),
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("click_to_load:index").path),
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

            from ludic.catalog.tables import Table, TableHead, TableRow
            from ludic.components import Blank, Component
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
                                    url=(
                                        f"{self.url_for(ContactsSlice).path}"
                                        f"?page={next_page}"
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
            t"First endpoint is function-based and is rendering the initial table "
            t"of contacts. We use the {Code('ContactsSlice.get()')} method to load "
            t"the first page. It would probably be better to separate this loading "
            t"to some handler function."
        ),
        Paragraph(
            t"The {Code('ContactsSlice')} endpoint-based component is loading the "
            t"table rows and implements two methods:"
        ),
        List(
            Item(
                Code("get"),
                " – handles the GET request which loads contacts from the database. "
                "The handler returns an instance of itself.",
            ),
            Item(
                Code("render"),
                t" – handles rendering of the table rows and the {Code('Load More')} "
                t"button. In order for everything to work properly, we render only "
                t"the table's rows while wrapping them in the {Code('Blank')} "
                t"component. This component does not render any HTML element, it's "
                t"just a wrapper when we want to render a list of elements.",
            ),
        ),
        Paragraph(
            t"Last, the {Code('ContactsTable')} class is a regular component that "
            t"renders the table's columns."
        ),
        Paragraph(
            t"The last remaining piece is the {Code('LoadMoreButton')} component which "
            t"triggers the {Code('GET')} request calling the {Code('ContactsSlice')} "
            t"method to load more contact data:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.attrs import Attrs
            from ludic.catalog.buttons import ButtonPrimary
            from ludic.components import ComponentStrict

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
                    )
            """,
            language="python",
        ),
        Paragraph(
            t"We use the HTMX swap operation to replace the button itself with a new "
            t"slice of contacts rendered by the {Code('ContactsSlice')} endpoint. "
            t"That is, the next page of rows as well as the button itself running the "
            t"HTMX operation. Since the {Code('ContactsSlice')} always bumps the "
            t"button link's page, we get the next page of contacts on every click."
        ),
        request=request,
        active_item="click_to_load",
        title="Ludic - Click To Load",
    )
