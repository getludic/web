"""The pages of the documentation, catalog and examples sections.

The menu, the sitemap, the search index and llms.txt are all built from this
list, so a new page needs to be added only here (and to its router).

The route name of a page is also the name of its module and endpoint function,
e.g. ``docs:getting_started`` is ``web.endpoints.docs.getting_started``.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PageInfo:
    name: str
    title: str
    description: str


@dataclass(frozen=True)
class Section:
    name: str
    title: str
    description: str
    pages: tuple[PageInfo, ...]


SECTIONS: tuple[Section, ...] = (
    Section(
        name="docs",
        title="Documentation",
        description="How to write components and build web apps with Ludic.",
        pages=(
            PageInfo(
                "index",
                "Introduction",
                "What Ludic is, its features, a comparison with htpy, FastHTML, "
                "tdom and Jinja2, requirements and installation.",
            ),
            PageInfo(
                "getting_started",
                "Getting Started",
                "Install Ludic, create a first app with LudicApp and run it.",
            ),
            PageInfo(
                "components",
                "Components",
                "HTML elements, Component and ComponentStrict, typed attributes, "
                "t-strings and the available helper types.",
            ),
            PageInfo(
                "styles",
                "Styles and Themes",
                "Component styles, the style element and attribute, loading and "
                "caching CSS, and themes.",
            ),
            PageInfo(
                "htmx",
                "HTMX Support",
                "Typed htmx attributes, loading htmx in a page, swap operations, "
                "response headers and inline JavaScript.",
            ),
            PageInfo(
                "web_framework",
                "Web Framework",
                "Routing, function and class-based endpoints, form parsers, error "
                "handlers, exceptions, WebSockets and testing.",
            ),
            PageInfo(
                "integrations",
                "Other Integrations",
                "Return Ludic elements from FastAPI and Django views.",
            ),
        ),
    ),
    Section(
        name="catalog",
        title="Catalog",
        description="Ready-made components in the ludic.catalog module.",
        pages=(
            PageInfo(
                "index",
                "Basics",
                "How the catalog works, how its CSS is loaded and how to create "
                "the base page component.",
            ),
            PageInfo(
                "layouts",
                "Layouts",
                "Stack, Box, Center, Cluster, Sidebar, Switcher, Cover, Grid and "
                "Frame layouts based on the Every Layout book.",
            ),
            PageInfo(
                "typography",
                "Typography",
                "Links, paragraphs, inline code, code blocks, key-value pairs, "
                "lists and headers with anchors.",
            ),
            PageInfo("buttons", "Buttons", "Button variants, button links and sizes."),
            PageInfo(
                "messages",
                "Messages",
                "Info, success, warning and danger message boxes.",
            ),
            PageInfo(
                "forms",
                "Forms",
                "Input, select, text area and choice fields, forms, and fields "
                "generated from an Attrs TypedDict.",
            ),
            PageInfo(
                "tables",
                "Tables",
                "Typed tables, and table rows generated from data.",
            ),
            PageInfo(
                "loaders",
                "Loaders",
                "A loading indicator and LazyLoader, which loads content after the "
                "page renders.",
            ),
        ),
    ),
    Section(
        name="examples",
        title="Examples",
        description="htmx patterns from htmx.org implemented with Ludic.",
        pages=(
            PageInfo(
                "index",
                "Components",
                "Custom components with styles: a link, a navigation and a search bar.",
            ),
            PageInfo(
                "complex_layout",
                "Complex Layout",
                "A page layout composed from the catalog layouts.",
            ),
            PageInfo(
                "bulk_update",
                "Bulk Update",
                "Activate or deactivate several table rows with one form.",
            ),
            PageInfo(
                "click_to_edit",
                "Click to Edit",
                "Switch a record to an edit form and save it with PUT.",
            ),
            PageInfo(
                "click_to_load",
                "Click to Load",
                "Load the next page of table rows with a button.",
            ),
            PageInfo(
                "delete_row",
                "Delete Row",
                "Delete a table row after a confirmation.",
            ),
            PageInfo(
                "edit_row",
                "Edit Row",
                "Edit a single table row inline.",
            ),
            PageInfo(
                "infinite_scroll",
                "Infinite Scroll",
                "Load more rows when the last one scrolls into view.",
            ),
            PageInfo(
                "lazy_loading",
                "Lazy Loading",
                "Load slow content after the page renders.",
            ),
            PageInfo(
                "cascading_selects",
                "FastAPI Example",
                "Cascading select fields in a FastAPI app.",
            ),
        ),
    ),
)


def get_section(name: str) -> Section:
    for section in SECTIONS:
        if section.name == name:
            return section
    raise KeyError(name)
