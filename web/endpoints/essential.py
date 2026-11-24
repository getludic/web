"""Essential pages like robots.txt and sitemap.xml"""

from html import escape

from ludic.web import LudicApp, Request
from starlette.responses import PlainTextResponse, Response

from .. import config
from ..navigation import SECTIONS

app = LudicApp()


@app.get("/robots.txt")
async def robots_txt() -> PlainTextResponse:
    """Generate robots.txt for search engine crawlers"""
    content = f"""User-agent: *
Allow: /

Sitemap: {config.HOME_URL}/sitemap.xml

# Crawl-delay for polite crawling
Crawl-delay: 1
"""
    return PlainTextResponse(content)


@app.get("/sitemap.xml")
async def sitemap_xml(request: Request) -> Response:
    """Generate XML sitemap for search engines"""
    paths = ["/"] + [
        request.url_path_for(f"{section.name}:{page.name}")
        for section in SECTIONS
        for page in section.pages
    ]
    urls = "".join(
        f"    <url><loc>{escape(config.HOME_URL + path)}</loc></url>\n"
        for path in paths
    )
    sitemap_content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}"
        "</urlset>\n"
    )

    return Response(
        content=sitemap_content,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=86400"},
    )
