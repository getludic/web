from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, h4
from ludic.web import Request

from web.pages import Page


def getting_started(request: Request) -> Page:
    return Page(
        H1("Getting Started"),
        Paragraph(
            "The fastest way to get started with a Ludic project is to use the "
            f"{Link(
               "Cookiecutter template",
               to="https://github.com/paveldedik/ludic-template")}. Follow the steps "
            "below to set up your project quickly."
        ),
        H2("Prerequisites"),
        Paragraph(
            "Before you begin, ensure you have the following installed on your machine:"
        ),
        List(
            Item(Link("Python 3.12", to="https://www.python.org/")),
            Item(Link("Poetry", to="https://python-poetry.org/")),
            Item(
                Link("Cookiecutter", to="https://cookiecutter.readthedocs.io"),
                " (optional for generating a new project)",
            ),
        ),
        H2("Installation Steps"),
        NumberedList(
            Item(
                b("Install Cookiecutter"),
                Paragraph(
                    "If you don't have the Cookiecutter library installed, you can "
                    "install it by running:"
                ),
                CodeBlock("pip install cookiecutter"),
                Paragraph(
                    "For more information, refer to the ",
                    Link(
                        "Cookiecutter documentation",
                        to="https://cookiecutter.readthedocs.io",
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
                CodeBlock("cookiecutter gh:paveldedik/ludic-template"),
            ),
            Item(
                b("Install Dependencies"),
                Paragraph(
                    "Navigate to your project directory and install the required "
                    "dependencies using Poetry:"
                ),
                CodeBlock("poetry install"),
            ),
            Item(
                b("Run the Project"),
                Paragraph(
                    "Start your project using Uvicorn with the following command:"
                ),
                CodeBlock("poetry run uvicorn src.main:app --reload"),
            ),
            Item(
                b("Access the Application"),
                Paragraph(
                    f"Open your browser and visit {Link(
                        "http://localhost:8000", to="http://localhost:8000")} to "
                    "see your running application."
                ),
            ),
        ),
        H2("Structure"),
        Paragraph(
            "The cookiecutter template creates a somewhat opinionated project "
            "structure, feel free to adjust or suggest a different one on GitHub. "
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
            "For bigger applications, this structure can look completely different. "
            "There is also a lot of modules missing - models, database connection, "
            "and so on. If you are just getting started, this is still a good starting "
            "point."
        ),
        h4(Code("pages.py")),
        Paragraph(
            "The idea is to write a couple of pages (regular components) rendering as "
            f"a valid HTML document - using the {Code("<html>")} root tag."
        ),
        h4(Code("endpoints")),
        Paragraph(
            "The endpoints module contains all the endpoints for the application. "
            "The index module contains endpoints rendering when user opens the site. "
            "It is the root of your web application. The errors module contains error "
            "handlers (displaying the 404 page, and so on)."
        ),
        h4(Code("components.py")),
        Paragraph(
            "Any component that you want to use in your application should be "
            f"registered here. For example, a {Code("Navigation")} component together "
            f"with its attributes could be registered in the {Code("components.py")} "
            "file."
        ),
        h4(Code("main.py")),
        Paragraph(
            f"The module instantiates the {Code("LudicApp")} class and registers "
            "routes (by importing the endpoints module)."
        ),
        H2("What's Next?"),
        Paragraph(
            "In the next sections of this documentation, you will learn more about "
            "how to write components, endpoints, and what kinds of other tools there "
            "are. You will also learn about the Catalog which can be used to very "
            "quickly create basic layout of your web application."
        ),
        request=request,
        active_item="getting_started",
        title="Ludic - Getting Started",
    )
