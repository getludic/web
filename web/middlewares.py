from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from .database import DB, init_contacts, init_db, init_people


class CookieStorageMiddleware(BaseHTTPMiddleware):
    COOKIE_STORAGE_KEY: str = "ludic-examples-state"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            db = DB.from_json(request.cookies[self.COOKIE_STORAGE_KEY])
        except (KeyError, TypeError):
            db = init_db()

        if not db.people:
            db.people = init_people()

        if not db.contacts:
            db.contacts = init_contacts()

        request.scope["db"] = db
        response = await call_next(request)

        data = request.scope["db"].to_json()
        response.set_cookie(self.COOKIE_STORAGE_KEY, data, max_age=3600)

        return response
