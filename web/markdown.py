"""Render the content of a documentation page as Markdown.

The converter walks the Ludic element tree of a page instead of its HTML, so
code blocks keep their language and their exact source. Live previews (layouts,
buttons, forms, lazy-loaded demos) are left out, because only their source code
is useful as text.
"""

from ludic.base import BaseElement
from ludic.catalog.headers import H1, H2, H3, H4
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.messages import Message, Title
from ludic.catalog.quotes import Quote
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.catalog.utils import remove_whitespaces
from ludic.html import a, b, br, code, em, h1, h2, h3, h4, i, li, ol, p, strong, ul

from . import config
from .components import Quote as SiteQuote

HEADINGS: dict[type[BaseElement], int] = {
    H1: 1,
    h1: 1,
    H2: 2,
    h2: 2,
    H3: 3,
    h3: 3,
    H4: 4,
    h4: 4,
}


def absolute_url(url: str) -> str:
    return f"{config.HOME_URL}{url}" if url.startswith("/") else url


def inline_code(text: str) -> str:
    fence = "``" if "`" in text else "`"
    padding = " " if text.startswith("`") or text.endswith("`") else ""
    return f"{fence}{padding}{text}{padding}{fence}"


def inline(node: object) -> str:
    """Render a node as Markdown text without line breaks between blocks."""
    if isinstance(node, str | int | float):
        return str(node)
    if not isinstance(node, BaseElement):
        return ""
    if isinstance(node, Code | code):
        return inline_code(node.text)
    content = "".join(inline(child) for child in node.children)
    if isinstance(node, Link):
        return link(content, node.attrs["to"])
    if isinstance(node, a):
        return link(content, str(node.attrs.get("href", "")))
    if isinstance(node, b | strong) and content.strip():
        return f"**{content.strip()}**"
    if isinstance(node, i | em) and content.strip():
        return f"*{content.strip()}*"
    if isinstance(node, br):
        return "  \n"
    return content


def link(text: str, url: str) -> str:
    if not url or url.startswith("#"):
        return text
    return f"[{text}]({absolute_url(url)})"


def indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def list_items(node: BaseElement, ordered: bool) -> str:
    items = []
    number = 1
    for child in node.children:
        if not isinstance(child, Item | li):
            continue
        marker = f"{number}. " if ordered else "- "
        number += 1
        inline_parts = []
        blocks = []
        for part in child.children:
            if isinstance(part, BaseElement) and is_block(part):
                blocks.append(block(part))
            else:
                inline_parts.append(inline(part))
        text = "".join(inline_parts).strip()
        item = marker + text
        for nested in filter(None, blocks):
            item += "\n\n" + indent(nested, " " * len(marker))
        items.append(item)
    return "\n".join(items)


def table(node: BaseElement) -> str:
    rows: list[list[str]] = []
    for child in node.children:
        if isinstance(child, TableHead | TableRow):
            rows.append([inline(cell).replace("|", "\\|") for cell in child.children])
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    lines = [
        "| " + " | ".join(rows[0]) + " |",
        "|" + "---|" * width,
        *("| " + " | ".join(row) + " |" for row in rows[1:]),
    ]
    return "\n".join(lines)


def message(node: BaseElement) -> str:
    parts = []
    for child in node.children:
        if isinstance(child, Title):
            parts.append(f"**{inline(child).strip()}**")
        elif isinstance(child, BaseElement) and is_block(child):
            parts.append(block(child))
        else:
            text = inline(child).strip()
            if text:
                parts.append(text)
    return indent("\n\n".join(parts), "> ").replace("\n\n", "\n>\n")


def quote(node: Quote | SiteQuote) -> str:
    if isinstance(node, SiteQuote):
        source: str | None = node.attrs["source"]
    else:
        source = node.attrs.get("source_text")
    text = "> " + inline(node).strip()
    return f"{text}\n>\n> — {source}" if source else text


def is_block(node: BaseElement) -> bool:
    """Whether the node needs its own lines inside a list item or a message."""
    return isinstance(
        node,
        tuple(HEADINGS)
        + (CodeBlock, List, NumberedList, ul, ol, Message, Table, Quote, SiteQuote),
    )


def code_block(node: CodeBlock) -> str:
    source = "".join(str(child) for child in node.children)
    if node.attrs.get("remove_whitespaces", True):
        source = remove_whitespaces(source)
    language = node.attrs.get("language", "")
    return f"```{language}\n{source.strip()}\n```"


def block(node: object) -> str:
    """Render a block-level node, or an empty string for a live preview."""
    match node:
        case str():
            return node.strip()
        case BaseElement() if type(node) in HEADINGS:
            return "#" * HEADINGS[type(node)] + " " + inline(node).strip()
        case CodeBlock():
            return code_block(node)
        case List() | ul() | NumberedList() | ol():
            return list_items(node, ordered=isinstance(node, NumberedList | ol))
        case Message():
            return message(node)
        case Table():
            return table(node)
        case Quote() | SiteQuote():
            return quote(node)
        case Paragraph() | p() | b() | strong() | i() | em():
            return inline(node).strip()
        case _:
            return ""


def heading_level(text: str) -> int:
    hashes = len(text) - len(text.lstrip("#"))
    return hashes if text[hashes : hashes + 1] == " " else 0


def to_markdown(children: tuple[object, ...]) -> str:
    blocks = [text for child in children if (text := block(child))]
    kept = []
    for text, following in zip(blocks, [*blocks[1:], "# "], strict=True):
        level = heading_level(text)
        # Drop headings of sections that held only a live preview, e.g. "## Demo".
        if level and 0 < heading_level(following) <= level:
            continue
        kept.append(text)
    return "\n\n".join(kept) + "\n"
