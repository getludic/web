"""llms.txt, llms-full.txt and a Markdown version of every documentation page.

See https://llmstxt.org for the format. Coding agents read these files instead
of the HTML pages, so they get the code samples without the live demos.
"""

import importlib
from collections.abc import Awaitable, Callable
from inspect import isawaitable

from ludic.web import LudicApp, Request
from ludic.web.exceptions import NotFoundError
from starlette.responses import PlainTextResponse

from web import config
from web.markdown import to_markdown
from web.navigation import SECTIONS, PageInfo, Section
from web.pages import Page

app = LudicApp()

MARKDOWN = "text/markdown; charset=utf-8"
CACHE_CONTROL = {"Cache-Control": "public, max-age=3600"}

SUMMARY = (
    "Ludic lets you write HTML as typed Python components. The type checker "
    "validates the markup, so wrong nesting, unknown attributes and missing "
    "arguments are caught before a page renders. Ludic only renders HTML, so it "
    "fits into Starlette, FastAPI, Django or any other framework, and it pairs "
    "with htmx."
)

RULES = (
    "Ludic 1.x needs Python 3.14+ and mixes text with elements in t-strings: "
    "`p(t\"Hello {b('World')}!\")`. Use f-strings only in projects on Ludic 0.5.x "
    "(Python 3.12 and 3.13), which renders elements inside f-strings.",
    'Set `plugins = ["ludic.mypy_plugin"]` for mypy and run mypy after changes. '
    "Only mypy with the plugin checks the attributes passed to components.",
    "Text children are escaped. Wrap only trusted HTML in `Safe`, never user input.",
    "The HTTP methods of an `Endpoint` (`get`, `post`, `put`, ...) are "
    "classmethods that usually return `Self`; `render()` builds the HTML.",
    "Read form data with a handler parameter typed `Parser[SomeAttrs]` and call "
    "`.validate()`, which returns the TypedDict or raises a 400 `ValidationError`.",
    "Use `request.url_path_for(...)` or the `.path` of `url_for(...)` in links and "
    "`hx_*` attributes, so a forged Host header cannot change them.",
    "Prefer the catalog (`ludic.catalog.pages`, `layouts`, `forms`, `tables`) to "
    "building pages from raw `div` elements.",
)

RESOURCES = (
    (
        "README",
        f"{config.GITHUB_REPO_URL}/blob/main/README.md",
        "Overview, type checking errors, framework integrations and a comparison "
        "with other libraries.",
    ),
    (
        "Agent skill: ludic-components",
        f"{config.GITHUB_REPO_URL}/blob/main/skills/ludic-components/SKILL.md",
        "How to write components, use the catalog and check the code with mypy.",
    ),
    (
        "Agent skill: ludic-web",
        f"{config.GITHUB_REPO_URL}/blob/main/skills/ludic-web/SKILL.md",
        "How to write endpoints, parse forms, return htmx responses and build safe "
        "URLs.",
    ),
    (
        "Examples on GitHub",
        f"{config.GITHUB_REPO_URL}/tree/main/examples",
        "Runnable htmx patterns written with Ludic.",
    ),
)


def html_path(request: Request, section: Section, page: PageInfo) -> str:
    return request.url_path_for(f"{section.name}:{page.name}")


def markdown_path(path: str) -> str:
    return f"{path}index.md" if path.endswith("/") else f"{path}.md"


async def render_page(request: Request, section: Section, page: PageInfo) -> Page:
    module = importlib.import_module(f"web.endpoints.{section.name}.{page.name}")
    endpoint: Callable[[Request], Page | Awaitable[Page]] = getattr(module, page.name)
    result = endpoint(request)
    return await result if isawaitable(result) else result


_markdown_cache: dict[tuple[str, str], str] = {}


async def page_markdown(request: Request, section: Section, page: PageInfo) -> str:
    key = (section.name, page.name)
    if key not in _markdown_cache:
        rendered = await render_page(request, section, page)
        url = f"{config.HOME_URL}{html_path(request, section, page)}"
        _markdown_cache[key] = f"{to_markdown(rendered.children)}\nSource: {url}\n"
    return _markdown_cache[key]


@app.get("/llms.txt")
def llms_txt(request: Request) -> PlainTextResponse:
    lines = [
        "# Ludic",
        "",
        f"> {SUMMARY}",
        "",
        "Rules for writing Ludic code:",
        "",
        *(f"- {rule}" for rule in RULES),
    ]
    for section in SECTIONS:
        lines += ["", f"## {section.title}", ""]
        for page in section.pages:
            url = config.HOME_URL + markdown_path(html_path(request, section, page))
            lines.append(f"- [{page.title}]({url}): {page.description}")
    lines += [
        "",
        "## Optional",
        "",
        f"- [All pages in one file]({config.HOME_URL}/llms-full.txt): The "
        "documentation, catalog and examples above as one Markdown file.",
        *(f"- [{title}]({url}): {text}" for title, url, text in RESOURCES),
    ]
    return PlainTextResponse("\n".join(lines) + "\n", headers=CACHE_CONTROL)


@app.get("/llms-full.txt")
async def llms_full_txt(request: Request) -> PlainTextResponse:
    parts = [f"# Ludic\n\n> {SUMMARY}\n"]
    for section in SECTIONS:
        for page in section.pages:
            parts.append(await page_markdown(request, section, page))
    return PlainTextResponse("\n---\n\n".join(parts), headers=CACHE_CONTROL)


@app.get("/{section_name}/{slug}.md")
async def page_md(request: Request, section_name: str, slug: str) -> PlainTextResponse:
    path = f"/{section_name}/" if slug == "index" else f"/{section_name}/{slug}"
    for section in SECTIONS:
        if section.name != section_name:
            continue
        for page in section.pages:
            if html_path(request, section, page) == path:
                content = await page_markdown(request, section, page)
                return PlainTextResponse(
                    content, media_type=MARKDOWN, headers=CACHE_CONTROL
                )
    raise NotFoundError("Page not found")
