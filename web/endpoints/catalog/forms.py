from typing import Annotated

from ludic.attrs import Attrs
from ludic.catalog.buttons import ButtonSuccess
from ludic.catalog.forms import (
    FieldMeta,
    Form,
    InputField,
    Option,
    SelectField,
    TextAreaField,
    create_fields,
)
from ludic.catalog.headers import H1, H2
from ludic.catalog.layouts import Cluster
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.web import Request

from web.pages import Page


class PersonAttrs(Attrs):
    first_name: Annotated[str, FieldMeta()]
    last_name: Annotated[str, FieldMeta()]


def forms(request: Request) -> Page:
    return Page(
        H1("Forms"),
        Paragraph(
            f"These components located in {Code("ludic.catalog.forms")} are in an "
            "experimental mode. There is the possibility to automatically create form "
            f"{Link("fields from annotations", to="#generating-form-fields")}, but it "
            "is far from production-ready."
        ),
        H2("Input Field"),
        Paragraph(
            f"The {Code("InputField")} component is the most basic form field. It "
            f"is a wrapper around the {Code("input")} HTML element which also "
            "generates a label if not disabled. Here is what it looks like:"
        ),
        InputField(
            name="sample-input-field",
            label="First Name",
            placeholder="Your First Name",
        ),
        CodeBlock(
            """
            from ludic.catalog.forms import InputField

            InputField(
                label="First Name",
                placeholder="Your First Name",
                name="sample-input-field",
            )
            """,
            language="python",
        ),
        Paragraph(
            "You can also create the input field without the label by not passing "
            f"the {Code("label")} attribute:"
        ),
        InputField(name="sample-input-field"),
        CodeBlock(
            """
            from ludic.catalog.forms import InputField

            InputField(
                name="sample-input-field",
            )
            """,
            language="python",
        ),
        H2("Select Field"),
        Paragraph(
            f"The {Code("SelectField")} component is a wrapper around the "
            f"{Code("select")} HTML element. It also generates a label if not "
            "disabled. Here is what it looks like:"
        ),
        SelectField(
            Option("Option 1"),
            Option("Option 2", selected=True),
            Option("Option 3"),
            label="Select Option",
            name="sample-select-field",
        ),
        CodeBlock(
            """
            from ludic.catalog.forms import SelectField, Option

            SelectField(
                Option("Option 1"),
                Option("Option 2", selected=True),
                Option("Option 3"),
                label="Select Option",
                name="sample-select-field",
            )
            """,
            language="python",
        ),
        H2("Text Area"),
        Paragraph(
            f"The {Code("TextAreaField")} component is a wrapper around the "
            f"{Code("textarea")} HTML element. It also generates a label if not "
            "disabled. Here is what it looks like:"
        ),
        TextAreaField(
            name="sample-text-area",
            label="Description",
        ),
        CodeBlock(
            """
            from ludic.catalog.forms import TextAreaField

            TextAreaField(
                name="sample-text-area",
                label="Description",
            )
            """,
            language="python",
        ),
        Paragraph(
            "Similarly as for the input field, you can create the text area without "
            "the label."
        ),
        H2("Form"),
        Paragraph(
            f"The {Code("Form")} component is a wrapper around the {Code("form")} "
            "HTML element. Here is a sample form:"
        ),
        Form(
            InputField(
                name="sample-input-field",
                label="First Name",
                placeholder="Your First Name",
            ),
            TextAreaField(
                name="sample-text-area",
                label="Description",
            ),
            Cluster(ButtonSuccess("Submit")),
        ),
        CodeBlock(
            """
            from ludic.catalog.buttons import ButtonSuccess
            from ludic.catalog.forms import Form, InputField, TextAreaField
            from ludic.catalog.layouts import Cluster

            Form(
                InputField(
                    name="sample-input-field",
                    label="First Name",
                    placeholder="Your First Name",
                ),
                TextAreaField(
                    name="sample-text-area",
                    label="Description",
                ),
                Cluster(ButtonSuccess("Submit")),
            )
            """,
            language="python",
        ),
        Paragraph(
            f"We use the {Code("Cluster")} component to create a form with multiple "
            f"input fields and buttons. this component is described in the {Link(
                "Layouts section", to=request.url_for("catalog:layouts"))}. "
            "You can also have the input field and the button aligned horizontally "
            "using this layout component:"
        ),
        Form(
            Cluster(
                InputField(placeholder="First Name"),
                SelectField(
                    Option("Age", disabled=True, selected=True),
                    Option("0-18"),
                    Option("18+"),
                ),
                ButtonSuccess("Submit"),
            )
        ),
        CodeBlock(
            """
            from ludic.catalog.buttons import ButtonSuccess
            from ludic.catalog.forms import Form, InputField, Option, SelectField
            from ludic.catalog.layouts import Cluster

            Form(
                Cluster(
                    InputField(placeholder="First Name"),
                    SelectField(
                        Option("Age", disabled=True, selected=True),
                        Option("0-18"),
                        Option("18+"),
                    ),
                    ButtonSuccess("Submit"),
                )
            )
            """,
            language="python",
        ),
        H2("Generating Form Fields"),
        Paragraph(
            "In some cases, the attributes of a component or class-based endpoint "
            "can be used to create form fields automatically using the "
            f"{Code("create_fields")} function. Here is an example:"
        ),
        Form(
            *create_fields(
                PersonAttrs(first_name="John", last_name="Doe"), spec=PersonAttrs
            ),
        ),
        CodeBlock(
            """
            from typing import Annotated

            from ludic.attrs import Attrs
            from ludic.catalog.forms import FieldMeta, create_fields

            class PersonAttrs(Attrs):
                first_name: Annotated[str, FieldMeta()]
                last_name: Annotated[str, FieldMeta()]

            person = PersonAttrs(first_name="John", last_name="Doe")
            fields = create_fields(person, spec=PersonAttrs)
            """,
            language="python",
        ),
        Paragraph(
            f"The {Code("create_fields")} function generates form fields from "
            "annotations. It generates only fields that are annotated with the "
            f"{Code("FieldMeta")} dataclass, which looks like this:"
        ),
        CodeBlock(
            """
            @dataclass
            class FieldMeta:
                label: str | Literal["auto"] | None = "auto"
                kind: Literal["input", "textarea", "checkbox"] = "input"
                type: Literal["text", "email", "password", "hidden"] = "text"
                attrs: InputAttrs | TextAreaAttrs | None = None
                parser: Callable[[Any], PrimitiveChildren] | None = None
            """,
            language="python",
        ),
        Paragraph(
            f"The {Code("parser")} attribute validates and parses the field. Here is "
            "how you would use it:"
        ),
        CodeBlock(
            """
            from typing import Annotated

            from ludic.attrs import Attrs
            from ludic.web.parsers import ValidationError
            from ludic.catalog.forms import FieldMeta

            def parse_email(email: str) -> str:
                if len(email.split("@")) != 2:
                    raise ValidationError("Invalid email")
                return email

            class CustomerAttrs(Attrs):
                id: str
                name: Annotated[
                    str,
                    FieldMeta(label="Email", parser=parse_email),
                ]
            """,
            language="python",
        ),
        Paragraph(
            f"Fields created with the {Code("create_fields")} function can be than "
            f"extracted from submitted form data using the {Link(
                "Parser class",
                to=f"{request.url_for("docs:web_framework").path}#parsers")}."
        ),
        request=request,
        active_item="forms",
    )
