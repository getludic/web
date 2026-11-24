import re

from starlette.testclient import TestClient

from web.navigation import SECTIONS
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
    "/docs/integrations/",
    "/examples/",
    "/examples/bulk-update/",
    "/examples/click-to-edit/",
    "/examples/click-to-load/",
    "/examples/delete-row/",
    "/examples/edit-row/",
    "/examples/infinite-scroll/",
    "/examples/lazy-loading/",
    "/examples/complex-layout/",
    "/examples/cascading-selects/",
    "/llms.txt",
    "/llms-full.txt",
    "/sitemap.xml",
    "/robots.txt",
    "/status/live/",
    "/status/ready/",
]


def test_all_endpoints() -> None:
    with TestClient(app) as client:
        for route in routes:
            assert client.get(route).status_code == 200


def test_every_page_has_markdown_and_is_in_llms_txt() -> None:
    with TestClient(app) as client:
        llms_txt = client.get("/llms.txt")
        assert llms_txt.status_code == 200
        assert llms_txt.text.startswith("# Ludic\n\n> ")

        for section in SECTIONS:
            for page in section.pages:
                path = app.url_path_for(f"{section.name}:{page.name}")
                assert client.get(path).status_code == 200
                markdown_path = (
                    f"{path}index.md" if path.endswith("/") else f"{path}.md"
                )
                assert f"https://getludic.dev{markdown_path})" in llms_txt.text

                response = client.get(markdown_path)
                assert response.status_code == 200
                assert response.headers["content-type"].startswith("text/markdown")
                assert f"Source: https://getludic.dev{path}\n" in response.text


def test_markdown_keeps_code_and_drops_live_demos() -> None:
    with TestClient(app) as client:
        text = client.get("/examples/click-to-edit.md").text
        assert text.startswith("# Click To Edit\n")
        assert "```python\nfrom typing import Annotated\n" in text
        assert "## Demo" not in text
        assert "<" not in text.split("```")[0]

        full = client.get("/llms-full.txt").text
        assert "# Click To Edit\n" in full
        assert "# Getting Started\n" in full


def test_unknown_markdown_page_is_404() -> None:
    with TestClient(app) as client:
        assert client.get("/docs/missing.md").status_code == 404
        assert client.get("/unknown/index.md").status_code == 404


def test_sitemap_lists_every_page() -> None:
    with TestClient(app) as client:
        sitemap = client.get("/sitemap.xml").text
        for section in SECTIONS:
            for page in section.pages:
                path = app.url_path_for(f"{section.name}:{page.name}")
                assert f"<loc>https://getludic.dev{path}</loc>" in sitemap


def test_table_of_contents_links_to_existing_headings() -> None:
    with TestClient(app) as client:
        for section in SECTIONS:
            for page in section.pages:
                path = app.url_path_for(f"{section.name}:{page.name}")
                html = client.get(path).text
                toc = html.split('class="table-of-contents"', 1)[1].split("</nav>")[0]
                targets = re.findall(r'href="#([^"]+)"', toc)
                for target in targets:
                    assert f'id="{target}"' in html, (path, target)


def test_every_page_links_its_markdown_version() -> None:
    with TestClient(app) as client:
        for section in SECTIONS:
            for page in section.pages:
                path = app.url_path_for(f"{section.name}:{page.name}")
                html = client.get(path).text
                markdown = f"{path}index.md" if path.endswith("/") else f"{path}.md"
                assert (
                    f'<link rel="alternate" type="text/markdown" href="{markdown}">'
                ) in html
                assert f'href="{markdown}">View as Markdown</a>' in html


def test_pages_have_light_and_dark_styles() -> None:
    with TestClient(app) as client:
        html = client.get("/docs/").text
        assert html.count("<style") == 3  # fonts, light theme, dark theme
        assert 'media="(prefers-color-scheme: dark)" id="ludic-dark-styles"' in html
        assert "html { color-scheme: light; }" in html
        assert "html { color-scheme: dark; }" in html
        assert 'class="color-scheme-toggle"' in html


def test_homepage_sections() -> None:
    with TestClient(app) as client:
        html = client.get("/").text
        assert "Typed HTML components in" in html
        assert 'id="frameworks"' in html
        assert html.count('class="tab-input"') == 4
        assert 'id="counter"' in html
        assert "Built for coding agents" in html
        assert 'href="/llms.txt"' in html
        assert "&lt;p&gt;Hello" not in html.split("<pre")[0]
        assert client.get("/code-samples/0").status_code == 404
