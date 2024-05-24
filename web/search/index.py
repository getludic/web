import math
from collections.abc import Callable
from typing import Any, Literal

from ludic.base import BaseElement
from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.utils import text_to_kebab
from ludic.components import Blank
from ludic.web import LudicApp, Request
from ludic.web.datastructures import URLPath
from starlette._utils import is_async_callable

from web.endpoints import catalog, docs, examples
from web.pages import Page

from .analysis import analyze
from .documents import Document


class Index:
    """Ludic Web search index."""

    index: dict[str, set[int]]
    documents: dict[int, Document]

    def __init__(self) -> None:
        self.index = {}
        self.documents = {}

    def index_document(self, document: Document) -> None:
        if document.id not in self.documents:
            self.documents[document.id] = document
            document.analyze()

        for token in analyze(document.fulltext):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(document.id)

    def document_frequency(self, token: str) -> int:
        return len(self.index.get(token, set()))

    def inverse_document_frequency(self, token: str) -> float:
        # Manning, Hinrich and Schütze use log10, so we do too, even though it
        # doesn't really matter which log we use anyway
        # https://nlp.stanford.edu/IR-book/html/htmledition/inverse-document-frequency-1.html
        return math.log10(len(self.documents) / self.document_frequency(token))

    def _results(self, analyzed_query: list[str]) -> list[set[int]]:
        return [self.index.get(token, set()) for token in analyzed_query]

    def search(
        self, query: str, search_type: Literal["AND", "OR"] = "AND", rank: bool = True
    ) -> list[Document]:
        """Search; this will return documents that contain words from the query.

        It can also rank the documents if requested (sets are fast, but unordered).

        Parameters:
          - query: the query string
          - search_type: ('AND', 'OR') do all query terms have to match, or just one
          - score: (True, False) if True, rank results based on TF-IDF score
        """
        if search_type not in ("AND", "OR"):
            return []

        analyzed_query = analyze(query)
        results = self._results(analyzed_query)
        if search_type == "AND":
            # all tokens must be in the document
            documents = [
                self.documents[doc_id] for doc_id in set.intersection(*results)
            ]
        if search_type == "OR":
            # only one token has to be in the document
            documents = [self.documents[doc_id] for doc_id in set.union(*results)]

        if rank:
            return self.rank(analyzed_query, documents)
        return documents

    def rank(
        self, analyzed_query: list[str], documents: list[Document]
    ) -> list[Document]:
        results: list[tuple[Document, float]] = []
        if not documents:
            return []

        for document in documents:
            score = 0.0
            for token in analyzed_query:
                tf = document.term_frequency(token)
                idf = self.inverse_document_frequency(token)
                score += tf * idf
            results.append((document, score))

        return [doc[0] for doc in sorted(results, key=lambda doc: doc[1], reverse=True)]


class _FakeRequest:
    def __init__(self, app: LudicApp) -> None:
        self.app = app

    def url_for(
        self, endpoint: Callable[[Request], Page] | str, *args: Any, **kwargs: Any
    ) -> URLPath:
        result = self.app.url_path_for(
            endpoint if isinstance(endpoint, str) else endpoint.__name__,
            *args,
            **kwargs,
        )
        result.path = result  # type: ignore
        return result

    def url_path_for(
        self, endpoint: Callable[[Request], Page] | str, *args: Any, **kwargs: Any
    ) -> URLPath:
        return self.app.url_path_for(
            endpoint if isinstance(endpoint, str) else endpoint.__name__,
            *args,
            **kwargs,
        )


async def build_index(app: LudicApp) -> Index:
    endpoints = [
        catalog.index.index,
        catalog.typography.typography,
        catalog.buttons.buttons,
        catalog.messages.messages,
        catalog.layouts.layouts,
        catalog.loaders.loaders,
        catalog.forms.forms,
        catalog.tables.tables,
        docs.index.index,
        docs.components.components,
        docs.getting_started.getting_started,
        docs.htmx.htmx,
        docs.styles.styles,
        docs.web_framework.web_framework,
        examples.index.index,
        examples.bulk_update.bulk_update,
        examples.click_to_load.click_to_load,
        examples.delete_row.delete_row,
        examples.edit_row.edit_row,
        examples.infinite_scroll.infinite_scroll,
        examples.lazy_loading.lazy_loading,
    ]
    indexer = Index()

    data: list[tuple[str, BaseElement, list[BaseElement]]] = []
    for endpoint in endpoints:
        _, _, mount_name, route_name = endpoint.__module__.split(".")

        if is_async_callable(endpoint):
            response = await endpoint(_FakeRequest(app))  # type: ignore
        else:
            response = endpoint(_FakeRequest(app))  # type: ignore

        if not isinstance(response, Page):
            continue

        for child in response.children:
            if isinstance(child, H1 | H2):
                data.append(
                    (
                        f"{app.url_path_for(f"{mount_name}:{route_name}")}#{text_to_kebab(child.text)}",
                        H3(child.text, anchor=False),
                        [],
                    )
                )
            elif data and isinstance(child, BaseElement):
                data[-1][2].append(child)

    for idx, (url, title, content) in enumerate(data):
        document = Document(id=idx, title=title, content=Blank(*content), url=url)
        indexer.index_document(document)

    return indexer
