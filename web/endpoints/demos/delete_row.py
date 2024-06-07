from typing import Self, override

from ludic.attrs import Attrs, GlobalAttrs
from ludic.catalog.buttons import ButtonDanger
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.web import Endpoint, LudicApp, Request
from ludic.web.exceptions import NotFoundError

from web.database import DB

app = LudicApp()


class PersonAttrs(Attrs):
    id: str
    name: str
    email: str
    active: bool


class PeopleAttrs(Attrs):
    people: list[PersonAttrs]


@app.get("/")
def index(request: Request) -> "PeopleTable":
    return PeopleTable.get(request)


@app.endpoint("/people/{id}")
class PersonRow(Endpoint[PersonAttrs]):
    @classmethod
    def delete(cls, request: Request, id: str) -> None:
        db: DB = request.scope["db"]
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
                "Delete", hx_delete=self.url_for(PersonRow), classes=["small"]
            ),
        )


@app.endpoint("/people/")
class PeopleTable(Endpoint[PeopleAttrs]):
    styles = {
        "tr.htmx-swapping td": {
            "opacity": "0",
            "transition": "opacity 1s ease-out",
        }
    }

    @classmethod
    def get(cls, request: Request) -> Self:
        db: DB = request.scope["db"]
        return cls(people=[person.to_dict() for person in db.people.values()])

    @override
    def render(self) -> Table[TableHead, PersonRow]:
        return Table[TableHead, PersonRow](
            TableHead("Name", "Email", "Active", ""),
            *(PersonRow(**person) for person in self.attrs["people"]),
            body_attrs=GlobalAttrs(
                hx_confirm="Are you sure?",
                hx_target="closest tr",
                hx_swap="outerHTML swap:1s",
            ),
            classes=["text-align-center"],
        )
