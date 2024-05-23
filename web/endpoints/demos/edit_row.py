from typing import Annotated, NotRequired, Self, override

from ludic.attrs import Attrs, HtmxAttrs
from ludic.catalog.buttons import (
    ButtonPrimary,
    ButtonSecondary,
    ButtonSuccess,
)
from ludic.catalog.forms import InputField
from ludic.catalog.layouts import Cluster
from ludic.catalog.tables import ColumnMeta, Table, TableHead, TableRow
from ludic.types import JavaScript
from ludic.web import Endpoint, LudicApp, Request
from ludic.web.exceptions import NotFoundError
from ludic.web.parsers import Parser

from web.database import DB

app = LudicApp()


class PersonAttrs(Attrs):
    id: NotRequired[str]
    name: Annotated[str, ColumnMeta()]
    email: Annotated[str, ColumnMeta()]


class PeopleAttrs(Attrs):
    people: list[PersonAttrs]


@app.get("/")
async def index(request: Request) -> "PeopleTable":
    return await PeopleTable.get(request)


@app.endpoint("/people/{id}")
class PersonRow(Endpoint[PersonAttrs]):
    on_click_script: JavaScript = JavaScript(
        """
        let editing = document.querySelector('.editing')

        if (editing) {
            alert('You are already editing a row')
        } else {
            htmx.trigger(this, 'edit')
        }
        """
    )

    @classmethod
    async def put(cls, request: Request, id: str, data: Parser[PersonAttrs]) -> Self:
        db: DB = request.scope["db"]
        person = db.people.get(id)

        if person is None:
            raise NotFoundError("Person not found")

        for attr, value in data.validate().items():
            setattr(person, attr, value)

        return cls(**person.to_dict())

    @classmethod
    async def get(cls, request: Request, id: str) -> Self:
        db: DB = request.scope["db"]
        person = db.people.get(id)

        if person is None:
            raise NotFoundError("Person not found")

        return cls(**person.to_dict())

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


@app.endpoint("/people/{id}/form")
class PersonForm(Endpoint[PersonAttrs]):
    @classmethod
    async def get(cls, request: Request, id: str) -> Self:
        db: DB = request.scope["db"]
        person = db.people.get(id)

        if person is None:
            raise NotFoundError("Person not found")

        return cls(**person.to_dict())

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
                classes=["small", "centered"],
            ),
            classes=["editing"],
        )


@app.endpoint("/people/")
class PeopleTable(Endpoint[PeopleAttrs]):
    @classmethod
    async def get(cls, request: Request) -> Self:
        db: DB = request.scope["db"]
        return cls(people=[person.to_dict() for person in db.people.values()])

    @override
    def render(self) -> Table[TableHead, PersonRow]:
        return Table[TableHead, PersonRow](
            TableHead("Name", "Email", "Action"),
            *(PersonRow(**person) for person in self.attrs["people"]),
            body_attrs=HtmxAttrs(hx_target="closest tr"),
            classes=["text-align-center"],
        )
