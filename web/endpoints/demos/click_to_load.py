from typing import Self, override

from ludic.attrs import Attrs
from ludic.catalog.buttons import ButtonPrimary
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.components import Blank, Component, ComponentStrict
from ludic.html import td
from ludic.types import URLType
from ludic.web import Endpoint, LudicApp
from ludic.web.datastructures import QueryParams

app = LudicApp()


class ContactAttrs(Attrs):
    id: str
    name: str
    email: str


class ContactsSliceAttrs(Attrs):
    page: int
    contacts: list[ContactAttrs]


class LoadMoreAttrs(Attrs):
    url: URLType


def load_contacts(page: int) -> list[ContactAttrs]:
    return [
        ContactAttrs(
            id=str(page * 10 + idx),
            email=f"void{page * 10 + idx}@null.org",
            name="Agent Smith",
        )
        for idx in range(10)
    ]


class LoadMoreButton(ComponentStrict[LoadMoreAttrs]):
    target: str = "replace-me"

    @override
    def render(self) -> ButtonPrimary:
        return ButtonPrimary(
            "Load More Agents...",
            hx_get=self.attrs["url"],
            hx_target=f"#{self.target}",
        )


@app.get("/")
async def index() -> "ContactsTable":
    return ContactsTable(await ContactsSlice.get(QueryParams(page=1)))


@app.endpoint("/contacts/")
class ContactsSlice(Endpoint[ContactsSliceAttrs]):
    @classmethod
    async def get(cls, params: QueryParams) -> Self:
        page = int(params.get("page", 1))
        return cls(page=page, contacts=load_contacts(page))

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
                        url=self.url_for(ContactsSlice).include_query_params(
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
