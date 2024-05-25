from ludic.catalog.headers import H1, H2, H3, H4
from ludic.catalog.lists import Item, List
from ludic.catalog.messages import MessageWarning, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, i
from ludic.web import Request

from web.pages import Page


def web_framework(request: Request) -> Page:
    return Page(
        H1("Web Framework"),
        Paragraph(
            f"The Ludic library provides wrappers around {Link(
                "Starlette", to="https://www.starlette.io/")} framework to make it "
            "easy to write asynchronous web applications based on HTMX and "
            "Ludic Components."
        ),
        Paragraph(
            f"Ludic includes an application class {Code("LudicApp")} that tight "
            "together all other functionality. Here is how you can create an instance "
            "of the class:"
        ),
        CodeBlock(
            """
            from ludic.web import LudicApp

            app = LudicApp()
            """,
            language="python",
        ),
        Paragraph(
            f"The {Code("LudicApp")} class supports the same parameters as the "
            f"{Code("Starlette")} class from the {i("Starlette")} framework."
        ),
        H2("Routing"),
        Paragraph(
            f"To register handlers in your app, you can use the {Code("routes")} "
            f"arguments of the {Code("LudicApp")} class like this:"
        ),
        CodeBlock(
            """
            from ludic.web import LudicApp, Request
            from ludic.web.routing import Route

            def homepage(request: Request) -> p:
                return p("Hello, world!")

            routes = [
                Route("/", homepage),
            ]

            app = LudicApp(debug=True, routes=routes)
            """,
            language="python",
        ),
        Paragraph(
            "Alternatively, you can use a method decorator to register an endpoint:"
        ),
        CodeBlock(
            """
            from ludic.web import LudicApp, Request
            from ludic.web.routing import Route

            app = LudicApp(debug=True)

            @app.get("/")
            def homepage(request: Request) -> p:
                return p("Hello, world!")
            """,
            language="python",
        ),
        H3("The Application Instance"),
        Paragraph(
            i("class"),
            " ",
            Code("ludic.app.LudicApp"),
            i(
                "(debug=False, routes=None, middleware=None, exception_handlers=None, "
                "on_startup=None, on_shutdown=None, lifespan=None)"
            ),
        ),
        Paragraph("Creates an application instance."),
        H4("Parameters"),
        Paragraph(
            f"The list of parameters can be found in the {Link(
                "Starlette documentation",
                to="https://www.starlette.io/applications/#instantiating-the-application")}."
        ),
        H4("Methods"),
        List(
            Item(
                Code("app.register_route"),
                i('path: str, method: str = "GET"'),
                " – decorator to register function based endpoint handler",
            ),
            Item(
                Code("app.get"),
                i("path: str, **kwargs: Any"),
                " – decorator to register function endpoint handling GET HTTP method",
            ),
            Item(
                Code("app.post"),
                i("path: str, **kwargs: Any"),
                " – decorator to register function endpoint handling POST HTTP method",
            ),
            Item(
                Code("app.put"),
                i("path: str, **kwargs: Any"),
                " – decorator to register function endpoint handling PUT HTTP method",
            ),
            Item(
                Code("app.patch"),
                i("path: str, **kwargs: Any"),
                " – decorator to register function endpoint handling PATCH HTTP method",
            ),
            Item(
                Code("app.delete"),
                i("path: str, **kwargs: Any"),
                " – decorator to register function endpoint handling DELETE HTTP ",
                "method",
            ),
            Item(
                Code("app.endpoint"),
                i("path: str"),
                " – decorator to register component based endpoint",
            ),
            Item(
                Code("app.add_route"),
                i("path: str, route: Callable[..., Any], method: str, **kwargs: Any"),
                " – register any endpoint handler",
            ),
            Item(
                Code("app.url_path_for"),
                i("name: str, /, **path_params: Any"),
                " – get URL path for endpoint of given name",
            ),
            Item(
                Code("app.exception_handler"),
                i("exc_class_or_status_code: int | type[Exception]"),
                " – register exception handler",
            ),
        ),
        H2("Endpoints"),
        Paragraph("There are three types of endpoints that you can create:"),
        List(
            Item(Link("Function-Based", to="#function-based")),
            Item(Link("Component-Based", to="#component-based")),
        ),
        H3("Function-Based"),
        Paragraph(
            "These are functions returning Ludic components, a tuple or the "
            f"{Link("Starlette's Response class", to="https://www.starlette.io/responses/")}."
        ),
        Paragraph("Here are some examples of function handlers registered in Ludic:"),
        CodeBlock(
            """
            from ludic.web.datastructures import FormData
            from ludic.web.exceptions import NotFoundError

            from your_app.database import db
            from your_app.pages import Page
            from your_app.models import Person
            from your_app.components import Header


            @app.get("/people/{id}")
            async def show_person(id: str) -> Page:
                person: Person = db.people.get(id)

                if person is None:
                    raise NotFoundError("Contact not found")

                return Page(
                    Header(person.name),
                    ...
                )


            @app.post("/people/")
            async def register_person(data: FormData) -> Page:
                person: Person = Person.objects.create(**data)
                return await show_person(person.id), 202
            """,
            language="python",
        ),
        H3("Component-Based"),
        Paragraph(
            "While it is possible to use function-based handlers everywhere, in the "
            "case of HTMX-based web applications, we want to also create a lot of "
            "endpoints rendering only sole form elements, tables, and so on. We don't "
            f"need to always return the whole HTML document in {Code("<html>")} tag. "
            "We could use function-based handlers for that, however, it is often "
            "better to think of endpoints as just another components."
        ),
        Paragraph(
            "Component-based endpoints can only have one generic argument which is "
            "the type of attributes. They cannot have children."
        ),
        Paragraph("Here is an example where we create two component-based endpoints:"),
        CodeBlock(
            """
            from ludic.web import Endpoint
            from ludic.web.datastructures import FormData

            from your_app.database import db
            from your_app.pages import Page
            from your_app.models import Person
            from your_app.components import Header, Body


            @app.get("/")
            async def index() -> Page:
                return Page(
                    Header("Click To Edit"),
                    Body(*[
                        await Contact.get(contact_id) for contact_id in db.contacts
                    ]),
                )


            @app.endpoint("/contacts/{id}")
            class Contact(Endpoint[ContactAttrs]):
                @classmethod
                async def get(cls, id: str) -> Self:
                    contact = db.contacts.get(id)
                    return cls(**contact.as_dict())

                @classmethod
                async def put(cls, id: str, data: FormData) -> Self:
                    contact = db.contacts.get(id)
                    contact.update(**data)
                    return await cls.get(id)

                @override
                def render(self) -> div:
                    return div(
                        Pairs(items=self.attrs.items()),
                        ButtonPrimary(
                            "Click To Edit",
                            hx_get=self.url_for(ContactForm),
                        ),
                        hx_target="this",
                    )


            @app.endpoint("/contacts/{id}/form/")
            class ContactForm(Endpoint[ContactAttrs]):
                @classmethod
                async def get(cls, id: str) -> Self:
                    contact = db.contacts.get(id)
                    return cls(**contact.as_dict())

                @override
                def render(self) -> Form:
                    return Form(
                        # ... form fields definition here ...,
                        ButtonPrimary("Submit"),
                        ButtonDanger("Cancel", hx_get=self.url_for(Contact)),
                        hx_put=self.url_for(Contact),
                        hx_target="this",
                    )
            """,
            language="python",
        ),
        Paragraph(
            "One benefit of this approach is that you can create components that "
            "generate the URL path for other component-based endpoints with the "
            f"{Code("url_for")} method. More about that in the next section."
        ),
        H3("Reverse URL Lookups"),
        Paragraph(
            "There are two possible ways to generate the URL for a particular route "
            "handled by an endpoint:"
        ),
        List(
            Item(Code("Request.url_for")),
            Item(Code("Endpoint.url_for")),
        ),
        b(Code("Request.url_for(endpoint: Callable[..., Any] | str, ...)")),
        Paragraph(
            f"This method is available on the {Code("ludic.web.requests.Request")} "
            f"object. It generates and {Code("URLPath")} object for a given endpoint."
        ),
        b(Code("Endpoint.url_for(endpoint: type[RoutedProtocol] | str, ...)")),
        Paragraph(
            "This method is available on a component-based endpoint. It has one small "
            f"advantage over the {Code("request")}'s method – if the destination "
            "component defines the same attributes, the path parameters are "
            "automatically extracted so you don't need to pass them via key-word "
            "arguments. Here are examples:"
        ),
        List(
            Item(
                f"{Code("ContactForm(...).url_for(Contact)")}"
                f" – Even though the {Code("ContactForm")} endpoint requires the "
                f"{Code("id")} path parameter, it is automatically extracted from "
                f"{Code("ContactForm(...).attrs")} since the {Code("ContactForm")} and "
                f"{Code("Contact")} share the same attributes – {Code("ContactAttrs")}."
            ),
            Item(
                "If these attribute types are not equal, you need to specify the URL "
                "path parameter explicitly, e.g. "
                f"{Code('ContactForm(...).url_for(Foo, id=self.attrs["foo_id"])')}.",
            ),
            Item(
                f"If the first argument to {Code("url_for")} is the name of the "
                "endpoint, you need to always specify the URL path parameters "
                "explicitly."
            ),
        ),
        H3("Handler Responses"),
        Paragraph(
            "Your handler is not required to return only a valid element or component, "
            "you can also modify headers, status code, or return a "
            f"{Code("JSONResponse")}:"
        ),
        CodeBlock(
            """
            from ludic import types
            from ludic.html import div

            @app.get("/")
            def index() -> tuple[div, types.Headers]:
                return div("Headers Example"), {"Content-Type": "..."}
            """,
            language="python",
        ),
        Paragraph(
            "When it comes to the handler's return type, you have the following "
            "options:"
        ),
        List(
            Item(Code("BaseElement"), " – any element or component"),
            Item(
                Code("tuple[BaseElement, int]"),
                " – any element or component and a status code",
            ),
            Item(
                Code("tuple[BaseElement, types.Headers]"),
                " – any element or component and headers as a dict",
            ),
            Item(
                Code("tuple[BaseElement, int, types.Headers]"),
                " – any element or component, status code, and headers",
            ),
            Item(
                Code("starlette.responses.Response"),
                f" – valid Starlette {Code("Response")} object",
            ),
        ),
        H3("Handler Arguments"),
        Paragraph(
            "Here is a list of arguments that your handlers can optionally define "
            "(they need to be correctly type-annotated):"
        ),
        List(
            Item(
                Code("<name>: <type>"),
                " if the endpoint accepts path parameters, they can be specified in ",
                "the handler's arguments",
            ),
            Item(
                Code("request: Request"),
                f" the Ludic's slightly modified {Code("ludic.web.requests.Request")} ",
                f"class based on {Link("Starlette's one", to="https://www.starlette.io/requests/")}",
            ),
            Item(
                Code("params: QueryParams"),
                " contain query string parameters and can be imported from ",
                Code("ludic.web.datastructures.QueryParams"),
            ),
            Item(
                Code("data: FormData"),
                " an immutable multi-dict, containing both file uploads and text input "
                "from form submission",
            ),
            Item(
                Code("headers: Headers"),
                " HTTP headers exposed as an immutable, case-insensitive, multi-dict",
            ),
        ),
        H2("Parsers"),
        MessageWarning(
            Title("Experimental"),
            "This module is in an experimental state. The API may change in the "
            "future.",
        ),
        Paragraph(
            f"The {Code("ludic.parsers")} module contains helpers for parsing "
            f"{Code("FormData")}. The way it works is that you define {Code("Attrs")} "
            f"class with {Code("Annotated")} arguments like here:"
        ),
        CodeBlock(
            """
            class PersonAttrs(Attrs):
                id: NotRequired[int]
                name: Annotated[str, parse_name]
                email: Annotated[str, parse_email]
            """,
            language="python",
        ),
        Paragraph(
            f"Now you can use the {Code("Parser")} class to annotate arguments of your "
            "handler. The parser will attempt to parse form data if any "
            f"{Code("Callable")} is found in the metadata argument of "
            f"{Code("Annotated")}:"
        ),
        CodeBlock(
            """
            from ludic.web.parsers import Parser

            @app.put("/people/{id}")
            async def update_person(cls, id: str, data: Parser[PersonAttrs]) -> div:
                person = db.people.get(id)
                person.update(data.validate())
                return div(...)  # return updated person
            """,
            language="python",
        ),
        Paragraph(
            f"The {Code("Parser.validate()")} uses {Link(
                "typeguard", to="https://typeguard.readthedocs.io/")} to validate the "
            "form data. If the validation fails, the method raises "
            f"{Code("ludic.parsers.ValidationError")} if the request's form data are "
            f"not valid. If unhandled, this results in {Code("403")} status code."
        ),
        H3("Parsing Collections"),
        Paragraph(
            f"You can also use the {Code("ListParser")} class to parse a list of data. "
            f"It parses form data in a way similar to the {Code("Parser")} class, "
            "however, it expects the form data to have the identifier column as key. "
            "For example, we want to parse a first and last name columns from a list "
            f"of people, here are the example form data the {Code("ListParser")} is "
            "able to handle:"
        ),
        CodeBlock(
            """
            first_name:id:1=Joe&
            first_name:id:2=Jane&
            last_name:id:1=Smith&
            last_name:id:2=Doe
            """
        ),
        Paragraph("This would be transformed in the following structure:"),
        CodeBlock(
            """
            [
                {"id": 1, "first_name": "Joe", "last_name": "Smith"},
                {"id": 2, "first_name": "Jane", "last_name": "Doe"},
            ]
            """,
            language="python",
        ),
        Paragraph(
            f"This is how you could use the {Code("ListParser")} to parse a list of "
            "this kind of data from your view:"
        ),
        CodeBlock(
            """
            from ludic.web.parsers import ListParser

            @app.put("/people/")
            async def update_people(cls, id: str, data: ListParser[PersonAttrs]) -> div:
                people.update(data.validate())
                return div(...)  # return updated people
            """,
            language="python",
        ),
        H2("Error Handlers"),
        Paragraph(
            "You can use error handlers for custom pages for non-ok HTTP status codes. "
            f"You can register a handler with the {Code("app.exception_handler")} "
            "decorator:"
        ),
        CodeBlock(
            """
            from your_app.pages import Page


            @app.exception_handler(404)
            async def not_found() -> Page:
                return Page(
                    Header("Page Not Found"),
                    Body(Paragraph("The page you are looking for was not found.")),
                )


            @app.exception_handler(500)
            async def server_error() -> Page:
                return Page(
                    Header("Server Error"),
                    Body(Paragraph("Server encountered an error during processing.")),
                )
            """,
            language="python",
        ),
        Paragraph(
            f"Optionally, you can use the {Code("request: Request")} and "
            f"{Code("exc: Exception")} arguments for the handler:"
        ),
        CodeBlock(
            """
            @app.exception_handler(500)
            async def server_error(request: Request, exc: Exception) -> Page: ...
            """,
            language="python",
        ),
        H2("Exceptions"),
        Paragraph(
            f"The {Code("ludic.web.exceptions")} contains a lot of useful exceptions "
            "that can be raised in your views and caught in your custom error handlers:"
        ),
        List(
            Item(
                Code("ClientError(HTTPException)"),
                f" – default status code {Code("400")}",
            ),
            Item(
                Code("BadRequestError(ClientError)"),
                f" – default status code {Code("400")}",
            ),
            Item(
                Code("UnauthorizedError(ClientError)"),
                f" – default status code {Code("401")}",
            ),
            Item(
                Code("PaymentRequiredError(ClientError)"),
                f" – default status code {Code("402")}",
            ),
            Item(
                Code("ForbiddenError(ClientError)"),
                f" – default status code {Code("403")}",
            ),
            Item(
                Code("NotFoundError(ClientError)"),
                f" – default status code {Code("404")}",
            ),
            Item(
                Code("MethodNotAllowedError(ClientError)"),
                f" – default status code {Code("405")}",
            ),
            Item(
                Code("TooManyRequestsError(ClientError)"),
                f" – default status code {Code("429")}",
            ),
            Item(
                Code("ServerError(HTTPException)"),
                f" – default status code {Code("500")}",
            ),
            Item(
                Code("InternalServerError(ServerError)"),
                f" – default status code {Code("500")}",
            ),
            Item(
                Code("NotImplementedError(ServerError)"),
                f" – default status code {Code("501")}",
            ),
            Item(
                Code("BadGatewayError(ServerError)"),
                f" – default status code {Code("502")}",
            ),
            Item(
                Code("ServiceUnavailableError(ServerError)"),
                f" – default status code {Code("503")}",
            ),
            Item(
                Code("GatewayTimeoutError(ServerError)"),
                f" – default status code {Code("504")}",
            ),
        ),
        H2("WebSockets"),
        Paragraph(
            "WebSockets support is not yet fully tested in Ludic. However, Starlette "
            "has good support for WebSockets so it should be possible to use Ludic as "
            "well."
        ),
        H2("Testing"),
        Paragraph(
            "Testing Ludic Web Apps is the same as testing Starlette apps which use a "
            f"{Code("TestClient")} class exposing the same interface as {Code("httpx")}"
            f" library. Read more about testing in the {Link(
                "Starlette documentation",to="https://www.starlette.io/testclient/")}."
        ),
        request=request,
        active_item="web_framework",
        title="Ludic - Web Framework",
    )
