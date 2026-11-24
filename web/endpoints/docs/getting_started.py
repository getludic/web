from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, NumberedList
from ludic.catalog.messages import MessageInfo
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, h4
from ludic.web import Request

from web.pages import Page


def getting_started(request: Request) -> Page:
    return Page(
        H1("Getting Started"),
        Paragraph(
            t"The fastest way to get started with a Ludic project is to use the "
            t"{
                Link('Cookiecutter template', to='https://github.com/getludic/template')
            }. Follow the steps "
            t"below to set up your project quickly."
        ),
        MessageInfo(
            t"{b('Note')}: This guide covers Ludic 1.0 which requires Python 3.14+ and "
            t"uses t-strings. If you're using Python 3.12 or 3.13, use Ludic 0.5.x "
            t"with f-strings instead. Install with {Code('--python 3.13')} and use "
            t"f-strings in your code.",
        ),
        H2("Installation Steps"),
        NumberedList(
            Item(
                b("Install UV Package Manager"),
                Paragraph(
                    "If you don't have UV installed yet, check the official ",
                    Link(
                        "installation instructions",
                        to="https://docs.astral.sh/uv/getting-started/installation/",
                    ),
                    ".",
                ),
            ),
            Item(
                b("Generate a Ludic Project"),
                Paragraph(
                    "Use the Cookiecutter template to create a new Ludic project. "
                    "Run the following command in your terminal:"
                ),
                CodeBlock("uvx cookiecutter gh:getludic/template"),
            ),
            Item(
                b("Install Dependencies"),
                Paragraph(
                    "Navigate to the new project's directory and install the required "
                    "dependencies using UV:"
                ),
                CodeBlock("uv sync --python 3.14"),
            ),
            Item(
                b("Run the Project"),
                Paragraph(
                    "Start your project using Uvicorn with the following command:"
                ),
                CodeBlock("uv run uvicorn src.main:app --reload"),
            ),
            Item(
                b("Access the Application"),
                Paragraph(
                    t"Open your browser and visit {
                        Link('http://localhost:8000', to='http://localhost:8000')
                    } to "
                    t"see your running application."
                ),
            ),
        ),
        H2("Structure"),
        Paragraph(
            "The cookiecutter template generates a somewhat opinionated project "
            "structure. Feel free to adjust it or suggest a different one on GitHub. "
            "Here is the structure:"
        ),
        CodeBlock(
            """
            .
            ├── src
            │    ├── __init__.py
            │    ├── endpoints
            │    │       ├── __init__.py
            |    |       ├── errors.py
            │    │       ├── index.py
            │    │       └── ...
            │    ├── components.py
            │    ├── main.py
            │    ├── pages.py
            │    └── ...
            ├── static
            ├── tests
            ├── README.md
            └── pyproject.toml
            """,
            language="bash",
        ),
        Paragraph(
            "For larger applications, the structure can vary significantly. "
            "Additionally, many modules are missing, such as models and database "
            "connections. However, if you're just beginning, this still serves as "
            "a good starting point."
        ),
        h4(Code("pages.py")),
        Paragraph(
            t"The idea is to create a few pages (regular components) that render as "
            t"valid HTML documents using the {Code('<html>')} root tag."
        ),
        h4(Code("endpoints")),
        Paragraph(
            "The endpoints module contains all the application's endpoints. The index "
            "module includes endpoints that render when users open the site, serving "
            "as the root of your web application. The errors module contains error "
            "handlers, such as displaying the 404 page."
        ),
        h4(Code("components.py")),
        Paragraph(
            t"Any component you want to use in your application should be registered "
            t"here. For example, a {Code('Navigation')} component and its attributes "
            t"could be registered in the {Code('components.py')} file."
        ),
        h4(Code("main.py")),
        Paragraph(
            t"The module instantiates the {Code('LudicApp')} class and registers "
            t"routes by importing the {Code('endpoints')} module."
        ),
        H2("What's Next?"),
        Paragraph(
            "In the following sections of this documentation, you will learn more "
            "about writing components and endpoints, as well as the various other "
            "tools available. You will also learn about the Catalog, which can be "
            "used to quickly create the basic layout of your web application."
        ),
        request=request,
        active_item="getting_started",
        title="Ludic - Getting Started",
    )
