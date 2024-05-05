import json
from dataclasses import asdict, dataclass
from typing import Any, Self


@dataclass
class Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ContactData(Model):
    id: str
    first_name: str
    last_name: str
    email: str


@dataclass
class PersonData(Model):
    id: str
    name: str
    email: str
    active: bool = True


@dataclass
class DB(Model):
    contacts: dict[str, ContactData]
    people: dict[str, PersonData]

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            contacts={k: ContactData(**v) for k, v in data.get("contacts", {}).items()},
            people={k: PersonData(**v) for k, v in data.get("people", {}).items()},
        )

    @classmethod
    def from_json(cls, data: str) -> Self:
        return cls.from_dict(json.loads(data))


def init_contacts() -> dict[str, ContactData]:
    return {
        "1": ContactData(
            id="1",
            first_name="John",
            last_name="Doe",
            email="qN6Z8@example.com",
        )
    }


def init_people() -> dict[str, PersonData]:
    return {
        "1": PersonData(
            id="1",
            name="Joe Smith",
            email="joe@smith.org",
            active=True,
        ),
        "2": PersonData(
            id="2",
            name="Angie MacDowell",
            email="angie@macdowell.org",
            active=True,
        ),
        "3": PersonData(
            id="3",
            name="Fuqua Tarkenton",
            email="fuqua@tarkenton.org",
            active=True,
        ),
        "4": PersonData(
            id="4",
            name="Kim Yee",
            email="kim@yee.org",
            active=False,
        ),
    }


def init_db() -> DB:
    return DB(contacts=init_contacts(), people=init_people())
