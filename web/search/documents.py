from collections import Counter
from dataclasses import dataclass

from ludic.base import BaseElement

from .analysis import analyze


@dataclass
class Document:
    """Ludic Web searchable document."""

    id: int
    title: BaseElement
    content: BaseElement
    url: str

    @property
    def fulltext(self) -> str:
        return " ".join([self.title.text, self.content.text])

    def analyze(self) -> None:
        self.term_frequencies = Counter(analyze(self.fulltext))

    def term_frequency(self, term: str) -> int:
        return self.term_frequencies.get(term, 0)

    def get_content(self, max_words: int) -> BaseElement:
        children = []
        words = 0

        for child in self.content.children:
            if isinstance(child, BaseElement):
                children.append(child)
                words += child.text.count(" ") + 1
            if words >= max_words:
                break

        return type(self.content)(*children, **self.content.attrs)
