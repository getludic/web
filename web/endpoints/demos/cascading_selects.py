from typing import Any, override

from fastapi import Depends, FastAPI
from ludic.catalog.forms import Option, SelectField, SelectFieldAttrs
from ludic.catalog.layouts import Stack
from ludic.components import Component
from ludic.contrib.fastapi import LudicRoute
from ludic.web import Request
from ludic.web.exceptions import NotFoundError

from web.database import DB as Database

app = FastAPI()
app.router.route_class = LudicRoute


def get_db(request: Request) -> Any:
    return request.scope["db"]


class CarSelect(Component[str, SelectFieldAttrs]):
    """Ludic element representing car select."""

    @override
    def render(self) -> SelectField:
        return SelectField(
            *[Option(child, value=child.lower()) for child in self.children],
            label=self.attrs.pop("label", "Car Manufacturer"),
            name="manufacturer",
            **self.attrs,
        )


class CarModelsSelect(Component[str, SelectFieldAttrs]):
    """Ludic element representing car models select."""

    @override
    def render(self) -> SelectField:
        return SelectField(
            *[Option(child, value=child.lower()) for child in self.children],
            label=self.attrs.pop("label", "Car Model"),
            id="models",
            **self.attrs,
        )


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


@app.get("/models/")
def models(
    manufacturer: str | None = None, db: Database = Depends(get_db)
) -> CarModelsSelect:
    if car := db.find_car_by_name(manufacturer):
        return CarModelsSelect(*car.models, label=None)  # type: ignore
    else:
        raise NotFoundError("Car could not be found")
