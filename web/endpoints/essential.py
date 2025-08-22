"""Essential pages like robots.txt and sitemap.xml"""

from ludic.web import LudicApp
from starlette.responses import PlainTextResponse, Response

from .. import config

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
async def sitemap_xml() -> Response:
    """Generate XML sitemap for search engines"""
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{config.HOME_URL}/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{config.HOME_URL}/docs</loc>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{config.HOME_URL}/docs/getting-started</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{config.HOME_URL}/catalog</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>{config.HOME_URL}/demos</loc>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
    <url>
        <loc>{config.HOME_URL}/examples</loc>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
</urlset>"""

    return Response(
        content=sitemap_content,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=86400"},
    )
