from typing import Annotated, NotRequired, Self, override

from ludic.catalog.buttons import Button, ButtonDanger, ButtonPrimary
from ludic.catalog.forms import FieldMeta, Form, create_fields
from ludic.catalog.items import Pairs
from ludic.catalog.layouts import Box, Cluster, Stack
from ludic.types import Attrs
from ludic.web import Endpoint, LudicApp, Request
from ludic.web.exceptions import NotFoundError
from ludic.web.parsers import Parser, ValidationError

from web.database import DB

app = LudicApp()


def email_validator(email: str) -> str:
    if len(email.split("@")) != 2:
        raise ValidationError("Invalid email")
    return email


class ContactAttrs(Attrs):
    id: NotRequired[str]
    first_name: Annotated[str, FieldMeta(label="First Name")]
    last_name: Annotated[str, FieldMeta(label="Last Name")]
    email: Annotated[
        str, FieldMeta(label="Email", type="email", parser=email_validator)
    ]


@app.get("/")
async def index(request: Request) -> Box:
    db: DB = request.scope["db"]
    return Box(*(Contact(**contact.to_dict()) for contact in db.contacts.values()))


@app.endpoint("/contacts/{id}")
class Contact(Endpoint[ContactAttrs]):
    @classmethod
    async def get(cls, request: Request, id: str) -> Self:
        db: DB = request.scope["db"]
        contact = db.contacts.get(id)

        if contact is None:
            raise NotFoundError("Contact not found")

        return cls(**contact.to_dict())

    @classmethod
    async def put(cls, request: Request, id: str, attrs: Parser[ContactAttrs]) -> Self:
        db: DB = request.scope["db"]
        contact = db.contacts.get(id)

        if contact is None:
            raise NotFoundError("Contact not found")

        for key, value in attrs.validate().items():
            setattr(contact, key, value)

        return cls(**contact.to_dict())

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
        )


@app.endpoint("/contacts/{id}/form")
class ContactForm(Endpoint[ContactAttrs]):
    @classmethod
    async def get(cls, request: Request, id: str) -> Self:
        db: DB = request.scope["db"]
        contact = db.contacts.get(id)

        if contact is None:
            raise NotFoundError("Contact not found")

        return cls(**contact.to_dict())

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
        )
