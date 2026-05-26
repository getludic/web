import hashlib
import time

try:
    from pyinstrument import Profiler
    from pyinstrument.renderers.html import HTMLRenderer
    from pyinstrument.renderers.speedscope import SpeedscopeRenderer
except ImportError:
    pass
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send

from .database import DB, init_contacts, init_db, init_people


class TrustForwardedHostMiddleware:
    """Rewrite Host header and scheme from X-Forwarded-* before the app sees it.

    Required when the app sits behind CloudFront → Lambda Function URL: the
    Function URL only accepts requests whose Host header matches its own
    hostname (SigV4 signing requires it), so CloudFront overwrites Host on
    the way to origin. Without this middleware, `request.url_for(...)` and
    any absolute URLs generated server-side would point at the raw Lambda
    URL instead of the public domain.

    Must be installed BEFORE any middleware that reads request.url.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            headers: dict[bytes, bytes] = dict(scope["headers"])
            forwarded_host = headers.get(b"x-forwarded-host")
            forwarded_proto = headers.get(b"x-forwarded-proto")

            if forwarded_host:
                scope["headers"] = [
                    (b"host", forwarded_host) if name == b"host" else (name, value)
                    for name, value in scope["headers"]
                ]
            if forwarded_proto:
                scope["scheme"] = forwarded_proto.decode("latin-1")

        await self.app(scope, receive, send)


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


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add essential security headers to all responses"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # Essential security headers
        response.headers.update(
            {
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
                "Content-Security-Policy": (
                    "default-src 'self'; "
                    "script-src 'self' 'unsafe-inline' 'unsafe-eval' unpkg.com; "
                    "style-src 'self' 'unsafe-inline' fonts.googleapis.com; "
                    "font-src 'self' fonts.gstatic.com; "
                    "img-src 'self' data: https: github.com; "
                    "frame-src 'self' ghbtns.com; "
                    "connect-src 'self'"
                ),
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "X-XSS-Protection": "1; mode=block",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
            }
        )

        return response


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Add performance optimizations including ETag support and monitoring"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)

        # Add ETag for caching
        if response.status_code == 200 and hasattr(response, "body"):
            content = getattr(response, "body", b"")
            if content:
                etag = hashlib.sha256(content).hexdigest()[:16]
                response.headers["ETag"] = f'"{etag}"'

                # Check if client has current version
                if_none_match = request.headers.get("If-None-Match")
                if if_none_match == f'"{etag}"':
                    response.status_code = 304
                    response.headers["Content-Length"] = "0"

        # Add cache control for static-like content
        if request.url.path.startswith(("/static", "/catalog", "/docs")):
            response.headers["Cache-Control"] = "public, max-age=3600"
        else:
            response.headers["Cache-Control"] = "public, max-age=300"

        # Performance timing header for monitoring
        duration = time.time() - start_time
        response.headers["X-Response-Time"] = f"{duration:.3f}s"

        return response
