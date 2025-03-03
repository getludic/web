from httpx import Response
from starlette.testclient import TestClient

from web.database import DB
from web.middlewares import CookieStorageMiddleware
from web.server import app


def remove_escape_sequences(string: str) -> str:
    return string.encode("utf-8").decode("unicode_escape").strip('"')


def get_db(response: Response) -> DB:
    data = response.cookies[CookieStorageMiddleware.COOKIE_STORAGE_KEY]
    return DB.from_json(remove_escape_sequences(data))


def test_bulk_update() -> None:
    with TestClient(app) as client:
        assert client.get("/demos/bulk-update").status_code == 200
        response = client.get("/demos/bulk-update/people/")
        assert response.status_code == 200

        db = get_db(response)
        assert db.people["1"].active
        assert db.people["2"].active
        assert db.people["3"].active
        assert not db.people["4"].active

        activate_data = {"active:id:1": "on", "active:id:2": "on"}
        response = client.post("/demos/bulk-update/people/", data=activate_data)
        assert response.status_code == 200

        db = get_db(response)
        assert db.people["1"].active
        assert db.people["2"].active
        assert not db.people["3"].active
        assert not db.people["4"].active


def test_click_to_edit() -> None:
    with TestClient(app) as client:
        assert client.get("/demos/click-to-edit/").status_code == 200
        assert client.get("/demos/click-to-edit/contacts/1").status_code == 200
        assert client.get("/demos/click-to-edit/contacts/1/form/").status_code == 200
        assert client.get("/demos/click-to-edit/contacts/123").status_code == 404

        response = client.get("/demos/click-to-edit/contacts/123/form/")
        assert response.status_code == 404

        db = get_db(response)
        assert db.contacts["1"].first_name == "John"

        edit_data = {
            "first_name": "Test",
            "last_name": "Doe",
            "email": "test@example.com",
        }
        response = client.put("/demos/click-to-edit/contacts/1", data=edit_data)
        assert response

        db = get_db(response)
        assert db.contacts["1"].first_name == "Test"


def test_click_to_load() -> None:
    with TestClient(app) as client:
        assert client.get("/demos/click-to-load/").status_code == 200
        assert client.get("/demos/click-to-load/contacts/").status_code == 200
        assert client.get("/demos/click-to-load/contacts/?page=2").status_code == 200


def test_delete_row() -> None:
    with TestClient(app) as client:
        assert client.get("/demos/delete-row/").status_code == 200
        assert client.get("/demos/delete-row/people/").status_code == 200
        assert client.delete("/demos/delete-row/people/1").status_code == 204

        response = client.delete("/demos/delete-row/people/123")
        assert response.status_code == 404
        assert get_db(response).people.get("1") is None


def test_edit_row() -> None:
    with TestClient(app) as client:
        assert client.get("/demos/edit-row/").status_code == 200
        assert client.get("/demos/edit-row/people/").status_code == 200
        assert client.get("/demos/edit-row/people/1").status_code == 200
        assert client.get("/demos/edit-row/people/1/form/").status_code == 200
        assert client.get("/demos/edit-row/people/123").status_code == 404

        response = client.get("/demos/edit-row/people/123/form/")
        assert response.status_code == 404
        assert get_db(response).people["1"].name == "Joe Smith"

        edit_data = {"name": "Test", "email": "test@example.com"}
        response = client.put("/demos/edit-row/people/1", data=edit_data)
        assert response.status_code == 200

        db = get_db(response)
        assert db.people["1"].name == "Test"
        assert db.people["1"].email == "test@example.com"


def test_lazy_loading() -> None:
    with TestClient(app) as client:
        assert client.get("/demos/lazy-loading/").status_code == 200
        response = client.get("/demos/lazy-loading/load/0")
        assert response.status_code == 200
        assert b"Content Loaded" in response.content


def test_infinite_scroll() -> None:
    with TestClient(app) as client:
        assert client.get("/demos/infinite-scroll/").status_code == 200
        assert client.get("/demos/infinite-scroll/contacts/").status_code == 200
        assert client.get("/demos/infinite-scroll/contacts/?page=2").status_code == 200


def test_cascading_selects() -> None:
    with TestClient(app) as client:
        assert client.get("/demos/cascading-selects/").status_code == 200
        assert client.get("/demos/cascading-selects/models/").status_code == 404
        assert (
            client.get("/demos/cascading-selects/models/?manufacturer=audi").status_code
            == 200
        )
