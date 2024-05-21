from ludic.catalog.headers import H2
from ludic.catalog.layouts import Box, Stack
from ludic.catalog.typography import Paragraph
from ludic.types import HXHeaders
from ludic.web import LudicApp, Request
from ludic.web.datastructures import FormData, Headers
from starlette.datastructures import URL
from starlette.responses import RedirectResponse

from web.components import SearchResult

app = LudicApp()


@app.post("/search/")
def search_docs(
    form: FormData, headers: Headers, request: Request
) -> tuple[Stack, HXHeaders] | RedirectResponse:
    current_url = URL(headers.get("HX-Current-Url", "/").split("#")[0])

    if query := form.get("search"):
        index = request.state.index
        search_results: list[SearchResult | Box] = [
            SearchResult(
                title=document.title,
                content=document.get_content(50),
                url=document.url,
            )
            for document in index.search(query)
        ]
        if not search_results:
            search_results = [
                Box(Paragraph("No results found for your search query.")),
            ]

        return (
            Stack(
                H2(f"Search results for “{query}”", anchor=False),
                *search_results,
                id="main-content",
            ),
            {"HX-Replace-Url": str(current_url.replace_query_params(search=query))},
        )
    else:
        return RedirectResponse(
            url=current_url,
            status_code=303,
            headers={"HX-Replace-Url": str(current_url)},
        )
