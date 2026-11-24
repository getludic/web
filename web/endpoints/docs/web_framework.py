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
            t"The Ludic library provides wrappers around {
                Link('Starlette', to='https://www.starlette.io/')
            } framework to make it "
            t"easy to write asynchronous web applications based on HTMX and "
            t"Ludic Components."
        ),
        Paragraph(
            t"Ludic includes an application class {Code('LudicApp')} that tight "
            t"together all other functionality. Here is how you can create an instance "
            t"of the class:"
        ),
        CodeBlock(
            """
            from ludic.web import LudicApp

            app = LudicApp()
            """,
            language="python",
        ),
        Paragraph(
            t"The {Code('LudicApp')} class supports the same parameters as the "
            t"{Code('Starlette')} class from the {i('Starlette')} framework."
        ),
        H2("Routing"),
        Paragraph(
            t"To register handlers in your app, you can use the {Code('routes')} "
            t"arguments of the {Code('LudicApp')} class like this:"
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
            t"The list of parameters can be found in the {
                Link(
                    'Starlette documentation',
                    to='https://www.starlette.io/applications/#instantiating-the-application',
                )
            }."
        ),
        H4("Methods"),
        List(
            Item(
                Code("app.register_route"),
                i('(path: str, method: str = "GET")'),
                " – decorator to register function based endpoint handler",
            ),
            Item(
                Code("app.get"),
                i("(path: str, **kwargs: Any)"),
                " – decorator to register function endpoint handling GET HTTP method",
            ),
            Item(
                Code("app.post"),
                i("(path: str, **kwargs: Any)"),
                " – decorator to register function endpoint handling POST HTTP method",
            ),
            Item(
                Code("app.put"),
                i("(path: str, **kwargs: Any)"),
                " – decorator to register function endpoint handling PUT HTTP method",
            ),
            Item(
                Code("app.patch"),
                i("(path: str, **kwargs: Any)"),
                " – decorator to register function endpoint handling PATCH HTTP method",
            ),
            Item(
                Code("app.delete"),
                i("(path: str, **kwargs: Any)"),
                " – decorator to register function endpoint handling DELETE HTTP ",
                "method",
            ),
            Item(
                Code("app.endpoint"),
                i("(path: str)"),
                " – decorator to register component based endpoint",
            ),
            Item(
                Code("app.add_route"),
                i("(path: str, route: Callable[..., Any], method: str, **kwargs: Any)"),
                " – register any endpoint handler",
            ),
            Item(
                Code("app.url_path_for"),
                i("(name: str, /, **path_params: Any)"),
                " – get URL path for endpoint of given name",
            ),
            Item(
                Code("app.exception_handler"),
                i("(exc_class_or_status_code: int | type[Exception])"),
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
            t"These are functions returning Ludic components, a tuple or the "
            t"{Link("Starlette's Response class", to='https://www.starlette.io/responses/')}."
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
            t"While it is possible to use function-based handlers everywhere, in the "
            t"case of HTMX-based web applications, we want to also create a lot of "
            t"endpoints rendering only sole form elements, tables, and so on. We don't "
            t"need to always return the whole HTML document in {Code('<html>')} tag. "
            t"We could use function-based handlers for that, however, it is often "
            t"better to think of endpoints as just another components."
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
                            hx_get=self.url_for(ContactForm).path,
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
                        ButtonDanger("Cancel", hx_get=self.url_for(Contact).path),
                        hx_put=self.url_for(Contact).path,
                        hx_target="this",
                    )
            """,
            language="python",
        ),
        Paragraph(
            t"One benefit of this approach is that you can create components that "
            t"generate the URL path for other component-based endpoints with the "
            t"{Code('url_for')} method. More about that in the next section."
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
            t"This method is available on the {Code('ludic.web.requests.Request')} "
            t"object. It generates and {Code('URLPath')} object for a given endpoint."
        ),
        MessageWarning(
            Title("Host header poisoning"),
            Paragraph(
                t"{Code('Request.url_for(...)')} returns an "
                t"{i('absolute')} URL whose scheme and host are derived from the "
                t"incoming request – ultimately from the HTTP {Code('Host')} header "
                t"(and {Code('X-Forwarded-*')} headers when proxy headers are "
                t"trusted). If your app accepts requests with an untrusted "
                t"{Code('Host')}, an attacker can poison every absolute URL you "
                t"render – including {Code('hx-get')} / {Code('hx-post')} attributes, "
                t"links, redirects, and links sent in outbound messages – pointing "
                t"the browser at an attacker-controlled domain."
            ),
            Paragraph("Mitigations:"),
            List(
                Item(
                    "Prefer ",
                    Code("request.url_path_for(...)"),
                    " – or ",
                    Code("request.url_for(...).path"),
                    " – for in-app links and HTMX attributes. Relative paths "
                    "cannot be poisoned and are usually what you want anyway.",
                ),
                Item(
                    "Install ",
                    Code("starlette.middleware.trustedhost.TrustedHostMiddleware"),
                    " with an explicit ",
                    Code("allowed_hosts"),
                    " list so the app rejects requests with a forged ",
                    Code("Host"),
                    " header before any handler runs.",
                ),
                Item(
                    "Behind a reverse proxy or CDN, configure ",
                    Code("ProxyHeadersMiddleware"),
                    " (or an equivalent) with a trusted-proxy allowlist so ",
                    Code("X-Forwarded-Host"),
                    " / ",
                    Code("X-Forwarded-Proto"),
                    " are only honored from your own infrastructure.",
                ),
            ),
            Paragraph(
                t"FastAPI users get the same exposure: the FastAPI integration "
                t"wraps the incoming request in Ludic's {Code('Request')}, so "
                t"{Code('Request.url_for(...)')} is reachable from FastAPI "
                t"handlers and the same advice applies.",
            ),
        ),
        b(Code("Endpoint.url_for(endpoint: type[RoutedProtocol] | str, ...)")),
        Paragraph(
            t"This method is available on a component-based endpoint. It has one small "
            t"advantage over the {Code('request')}'s method – if the destination "
            t"component defines the same attributes, the path parameters are "
            t"automatically extracted so you don't need to pass them via key-word "
            t"arguments. Here are examples:"
        ),
        List(
            Item(
                t"{Code('ContactForm(...).url_for(Contact)')}"
                t" – Even though the {Code('ContactForm')} endpoint requires the "
                t"{Code('id')} path parameter, it is automatically extracted from "
                t"{Code('ContactForm(...).attrs')} since the {Code('ContactForm')} and "
                t"{Code('Contact')} share the same attributes – {Code('ContactAttrs')}."
            ),
            Item(
                t"If these attribute types are not equal, you need to specify the URL "
                t"path parameter explicitly, e.g. "
                t"{Code('ContactForm(...).url_for(Foo, id=self.attrs["foo_id"])')}.",
            ),
            Item(
                t"If the first argument to {Code('url_for')} is the name of the "
                t"endpoint, you need to always specify the URL path parameters "
                t"explicitly."
            ),
        ),
        H3("Handler Responses"),
        Paragraph(
            t"Your handler is not required to return only a valid element or "
            t"component, you can also modify headers, status code, or return a "
            t"{Code('JSONResponse')}:"
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
                t" – valid Starlette {Code('Response')} object",
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
                t" the Ludic's slightly modified {Code('ludic.web.requests.Request')} ",
                t"class based on {Link("Starlette's one", to='https://www.starlette.io/requests/')}",
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
            t"The {Code('ludic.parsers')} module contains helpers for parsing "
            t"{Code('FormData')}. The way it works is that you define {Code('Attrs')} "
            t"class with {Code('Annotated')} arguments like here:"
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
            t"Now you can use the {Code('Parser')} class to annotate arguments of your "
            t"handler. The parser will attempt to parse form data if any "
            t"{Code('Callable')} is found in the metadata argument of "
            t"{Code('Annotated')}:"
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
            t"The {Code('Parser.validate()')} uses {
                Link('typeguard', to='https://typeguard.readthedocs.io/')
            } to validate the "
            t"form data. If the validation fails, the method raises "
            t"{Code('ludic.parsers.ValidationError')} if the request's form data are "
            t"not valid. If unhandled, this results in {Code('403')} status code."
        ),
        H3("Parsing Collections"),
        Paragraph(
            t"You can also use the {Code('ListParser')} class to parse a list of data. "
            t"It parses form data in a way similar to the {Code('Parser')} class, "
            t"however, it expects the form data to have the identifier column as key. "
            t"For example, we want to parse a first and last name columns from a list "
            t"of people, here are the example form data the {Code('ListParser')} is "
            t"able to handle:"
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
            t"This is how you could use the {Code('ListParser')} to parse a list of "
            t"this kind of data from your view:"
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
            t"You can use error handlers for custom pages for non-ok HTTP status "
            t"codes. You can register a handler with the "
            t"{Code('app.exception_handler')} decorator:"
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
            t"Optionally, you can use the {Code('request: Request')} and "
            t"{Code('exc: Exception')} arguments for the handler:"
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
            t"The {Code('ludic.web.exceptions')} contains a lot of useful exceptions "
            t"that can be raised in your views and caught in your custom error "
            t"handlers:"
        ),
        List(
            Item(
                Code("ClientError(HTTPException)"),
                t" – default status code {Code('400')}",
            ),
            Item(
                Code("BadRequestError(ClientError)"),
                t" – default status code {Code('400')}",
            ),
            Item(
                Code("UnauthorizedError(ClientError)"),
                t" – default status code {Code('401')}",
            ),
            Item(
                Code("PaymentRequiredError(ClientError)"),
                t" – default status code {Code('402')}",
            ),
            Item(
                Code("ForbiddenError(ClientError)"),
                t" – default status code {Code('403')}",
            ),
            Item(
                Code("NotFoundError(ClientError)"),
                t" – default status code {Code('404')}",
            ),
            Item(
                Code("MethodNotAllowedError(ClientError)"),
                t" – default status code {Code('405')}",
            ),
            Item(
                Code("TooManyRequestsError(ClientError)"),
                t" – default status code {Code('429')}",
            ),
            Item(
                Code("ServerError(HTTPException)"),
                t" – default status code {Code('500')}",
            ),
            Item(
                Code("InternalServerError(ServerError)"),
                t" – default status code {Code('500')}",
            ),
            Item(
                Code("NotImplementedError(ServerError)"),
                t" – default status code {Code('501')}",
            ),
            Item(
                Code("BadGatewayError(ServerError)"),
                t" – default status code {Code('502')}",
            ),
            Item(
                Code("ServiceUnavailableError(ServerError)"),
                t" – default status code {Code('503')}",
            ),
            Item(
                Code("GatewayTimeoutError(ServerError)"),
                t" – default status code {Code('504')}",
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
            t"Testing Ludic Web Apps is the same as testing Starlette apps which use a "
            t"{Code('TestClient')} class exposing the same interface as {Code('httpx')}"
            t" library. Read more about testing in the {
                Link(
                    'Starlette documentation', to='https://www.starlette.io/testclient/'
                )
            }."
        ),
        request=request,
        active_item="web_framework",
        title="Ludic - Web Framework",
    )
