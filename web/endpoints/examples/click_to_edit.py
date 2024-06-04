from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.web import Request

from web import config
from web.pages import Page


async def click_to_edit(request: Request) -> Page:
    return Page(
        H1("Click To Edit"),
        Paragraph(
            "The click to edit pattern provides a way to offer inline editing "
            "of all or part of a record without a page refresh. In this example, "
            "we create a customer which we'll be able to edit."
        ),
        List(
            Item(
                Link(
                    "Full Code at GitHub",
                    to=f"{config.GITHUB_REPO_URL}/blob/main/examples/click_to_edit.py",
                )
            ),
            Item(
                Link(
                    "Source at htmx.org", to="https://htmx.org/examples/click-to-edit/"
                )
            ),
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("click_to_edit:index")),
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
        active_item="click_to_edit",
        title="Ludic - Click To Edit",
    )
