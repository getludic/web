from starlette.testclient import TestClient

from web.server import app

routes: list[str] = [
    "/",
    "/catalog/",
    "/catalog/buttons/",
    "/catalog/forms/",
    "/catalog/layouts/",
    "/catalog/loaders/",
    "/catalog/messages/",
    "/catalog/tables/",
    "/catalog/typography/",
    "/docs/",
    "/docs/getting-started/",
    "/docs/components/",
    "/docs/htmx/",
    "/docs/styles/",
    "/docs/web-framework/",
    "/examples/",
    "/examples/bulk-update/",
    "/examples/click-to-edit/",
    "/examples/click-to-load/",
    "/examples/delete-row/",
    "/examples/edit-row/",
    "/examples/infinite-scroll/",
    "/examples/lazy-loading/",
    "/status/live/",
    "/status/ready/",
]


def test_all_endpoints() -> None:
    with TestClient(app) as client:
        for route in routes:
            assert client.get(route).status_code == 200
