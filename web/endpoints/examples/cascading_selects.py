from ludic.catalog.headers import H1, H2
from ludic.catalog.lists import Item, List
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b
from ludic.web import Request

from web import config
from web.pages import Page


async def cascading_selects(request: Request) -> Page:
    return Page(
        H1("Cascading Selects (FastAPI)"),
        Paragraph(
            f"The cascading selects example uses {b("FastAPI")} to implement two "
            "selects. First one is a simple select of a car's manufacturer. Second "
            "select's values are based on the option chosen by the first one."
        ),
        List(
            Item(
                Link(
                    "Full Code at GitHub",
                    to=f"{config.GITHUB_REPO_URL}/blob/main/examples/fastapi_example.py",
                )
            ),
            Item(
                Link("Source at htmx.org", to="https://htmx.org/examples/value-select/")
            ),
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for("cascading_selects:index")),
        H2("Implementation"),
        Paragraph(
            "In this example, we are using FastAPI instead of Starlette. So we need to "
            f"install ludic with the {Code('fastapi')} extra:"
        ),
        CodeBlock(
            """
            pip install ludic[fastapi]
            """
        ),
        Paragraph("Next step is to import and set up all the necessary classes:"),
        CodeBlock(
            """
            from fastapi import FastAPI
            from ludic.contrib.fastapi import LudicRoute

            app = FastAPI()
            app.router.route_class = LudicRoute
            """,
            language="python",
        ),
        Paragraph(
            "Now let us set up a database. In this case, we are using a fake database "
            "of data classes. In real example, you might want to use e.g. SQLAlchemy "
            "ORM session. Anyway, here is what it might look like:"
        ),
        CodeBlock(
            """
            def get_session(request: Request) -> Database:
                return request.scope["db"]  # this is a fake database
            """,
            language="python",
        ),
        Paragraph(
            "Next step is to create our select boxes. The first one will be selecting "
            "manufacturers, while the second car's models:"
        ),
        CodeBlock(
            """
            from typing import override

            from ludic.catalog.forms import Option, SelectField, SelectFieldAttrs
            from ludic.catalog.layouts import Stack
            from ludic.components import Component

            class CarSelect(Component[str, SelectFieldAttrs]):
                \"\"\"Ludic element representing car select.\"\"\"

                @override
                def render(self) -> SelectField:
                    return SelectField(
                        *[
                            Option(child, value=child.lower())
                            for child in self.children
                        ],
                        label=self.attrs.pop("label", "Car Manufacturer"),
                        name="manufacturer",
                        **self.attrs,
                    )


            class CarModelsSelect(Component[str, SelectFieldAttrs]):
                \"\"\"Ludic element representing car models select.\"\"\"

                @override
                def render(self) -> SelectField:
                    return SelectField(
                        *[
                            Option(child, value=child.lower())
                            for child in self.children
                        ],
                        label=self.attrs.pop("label", "Car Model"),
                        id="models",
                        **self.attrs,
                    )
            """,
            language="python",
        ),
        Paragraph(
            "Finally, we can implement the FastAPI view which renders the initial "
            "page containing two select boxes:"
        ),
        CodeBlock(
            """
            from fastapi import Depends
            from ludic.web import Request  # FastAPI is configured to use our custom
                                           # Request object

            from my_app import Database, get_db
            from my_app.components import CarSelect, CarModelsSelect

            @app.get("/")
            def index(request: Request, db: Database = Depends(get_db)) -> Stack:
                return Stack(
                    CarSelect(
                        *db.find_all_cars_names(),
                        hx_get=request.url_for(models),
                        hx_target="#models",
                    ),
                    CarModelsSelect(*db.find_first_car().models),
                )
            """,
            language="python",
        ),
        Paragraph(
            "We also need to implement the view that returns the car models options:"
        ),
        CodeBlock(
            """
            from ludic.web.exceptions import NotFoundError
            # ... already imported stuff skipped

            @app.get("/models/")
            def models(
                manufacturer: str | None = None, db: Database = Depends(get_db)
            ) -> CarModelsSelect:
                if car := db.find_car_by_name(manufacturer):
                    return CarModelsSelect(*car.models, label=None)
                else:
                    raise NotFoundError("Car could not be found")
            """,
            language="python",
        ),
        request=request,
        active_item="cascading_selects",
        title="Ludic - Cascading Selects",
    )
