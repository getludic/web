try:
    from pyinstrument import Profiler
    from pyinstrument.renderers.html import HTMLRenderer
    from pyinstrument.renderers.speedscope import SpeedscopeRenderer
except ImportError:
    pass
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


class ProfileMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Profile the current request

        Taken from
        https://blog.balthazar-rouberol.com/how-to-profile-a-fastapi-asynchronous-request
        """
        # we map a profile type to a file extension, as well as a pyinstrument profile
        # renderer
        profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
        profile_type_to_renderer = {
            "html": HTMLRenderer,
            "speedscope": SpeedscopeRenderer,
        }

        # if the `profile=true` HTTP query argument is passed, we profile the request
        if request.query_params.get("profile", False):
            # The default profile format is speedscope
            profile_type = request.query_params.get("profile_format", "speedscope")

            # we profile the request along with all additional middlewares, by
            # interrupting the program every 1ms1 and records the entire stack at
            # that point
            with Profiler(interval=0.001, async_mode="enabled") as profiler:
                response = await call_next(request)

            # we dump the profiling into a file
            extension = profile_type_to_ext[profile_type]
            renderer = profile_type_to_renderer[profile_type]()
            with open(f"profile.{extension}", "w") as out:
                out.write(profiler.output(renderer=renderer))
            return response

        # Proceed without profiling
        return await call_next(request)
