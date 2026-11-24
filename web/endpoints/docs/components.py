from ludic.catalog.headers import H1, H2, H3, H4
from ludic.catalog.lists import Item, List
from ludic.catalog.messages import Message, MessageWarning, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b, i
from ludic.web import Request

from web.pages import Page


def components(request: Request) -> Page:
    return Page(
        H1("Components"),
        Paragraph(
            "In Ludic, you can create components similar to React components. "
            "These components don't have anything like a state similar to React, "
            "but they do consist of children and attributes."
        ),
        H2("Key Concepts"),
        List(
            Item(
                t"{b('Components')}: a component is a reusable chunk of code that "
                t"defines a piece of your user interface. Think of it like a blueprint "
                t"for an HTML element, but more powerful."
            ),
            Item(
                t"{b('Elements')}: these represent the individual HTML tags (like "
                t"{Code('<a>')}, {Code('<div>')}, {Code('<h1>')}, etc.) that make up "
                t"the structure of your page."
            ),
            Item(
                t"{b('Attributes')}: These help define the properties on your "
                t"components and elements. They let you modify things like a link's "
                t"destination, text color, or an element's size."
            ),
            Item(
                t"{b('Hierarchy')}: Components can contain other components or "
                t"elements, creating a tree-like structure."
            ),
            Item(
                t"{b('Types')}: A safety net to help you write correct code, "
                t"preventing errors just like making sure LEGO pieces fit together "
                t"properly."
            ),
        ),
        H2("Types of Components"),
        List(
            Item(
                t"{b('Regular')}: These are flexible, letting you have multiple "
                t"children of any type."
            ),
            Item(
                t"{b('Strict')}: Perfect for when you need precise control over the "
                t"structure of your component – like a table where you must have a "
                t"head and a body."
            ),
        ),
        H2("Regular Components"),
        Paragraph(
            t"Let's break down a simplified version of the {Code('Link')} component:"
        ),
        CodeBlock(
            """
            from typing import override
            from ludic import Attrs, Component

            class LinkAttrs(Attrs):
                to: str

            class Link(Component[str, LinkAttrs]):
                @override
                def render(self):
                    return a(
                        *self.children,
                        href=self.attrs["to"],
                        style={"color": "#abc"},
                    )
            """,
            language="python",
        ),
        List(
            Item(
                t"{i('HTML Rendering')}: This component renders as the following HTML "
                t"element:",
                List(Item(Code('<a href="..." style="color:#abc">...</a>'))),
            ),
            Item(
                t"{i('Type Hints')}: {Code('Component[str, LinkAttrs]')} provides type "
                t"safety:",
                List(
                    Item(
                        t"{i('str')}: Enforces that all children of the component "
                        t"must be strings"
                    ),
                    Item(
                        t"{i('LinkAttrs')}: Ensures the required to attribute is "
                        t"present"
                    ),
                ),
            ),
            Item(
                t"{i('Attributes')}: {Code('LinkAttrs')} inherits from "
                t"{Code('Attrs')}, which is a {Code('TypedDict')} "
                t"(a dictionary with defined types for its keys)",
            ),
        ),
        Paragraph("The component would be instantiated like this:"),
        CodeBlock('Link("here", to="https://example.org")', language="python"),
        Paragraph(
            "Static type checkers will validate that you're providing the "
            "correct arguments and their types."
        ),
        H3("Multiple Children"),
        Paragraph(
            t"The current definition doesn't strictly enforce a single child. "
            t"This means you could technically pass multiple strings "
            t"({Code('Link("a", "b")')}). To create a stricter component, inherit "
            t"from {Code('ComponentStrict')}: This subclass of Component allows for "
            t"finer control over children. More about this in the next section."
        ),
        H2("Strict Components"),
        Paragraph(
            t"Strict components offer more precise control over the types and "
            t"structures of their children compared to regular components. Let's "
            t"illustrate this with a simplified {Code('Table')} component:"
        ),
        CodeBlock(
            """
            from ludic.attrs import GlobalAttrs
            from ludic.html import thead, tbody, tr

            class TableHead(ComponentStrict[tr, GlobalAttrs]):
                @override
                def render(self) -> thead:
                    return thead(*self.children, **self.attrs)

            class TableBody(ComponentStrict[*tuple[tr, ...], GlobalAttrs]):
                @override
                def render(self) -> tbody:
                    return tbody(*self.children, **self.attrs)

            class Table(ComponentStrict[TableHead, TableBody, GlobalAttrs]):
                @override
                def render(self) -> table:
                    return table(
                        self.children[0],
                        self.children[1],
                        **self.attrs,
                    )
            """,
            language="python",
        ),
        b("Explanation"),
        List(
            Item(
                t"{i('Strictness')}: The {Code('ComponentStrict')} class allows you to "
                t"enforce the exact types and order of children."
            ),
            Item(
                t"{i('Table Structure')}:",
                List(
                    Item(
                        t"{Code('Table')}: Expects precisely two children: a "
                        t"{Code('TableHead')} followed by a {Code('TableBody')}."
                    ),
                    Item(
                        t"{Code('TableHead')}: Accepts only a single {Code('tr')} "
                        t"(table row) element as its child."
                    ),
                    Item(
                        t"{Code('TableBody')}: Accepts a variable number of "
                        t"{Code('tr')} elements as children."
                    ),
                ),
            ),
            Item(
                t"{i('Type Hints')}: The {Code('*tuple[tr, ...]')} syntax indicates "
                t"that {Code('TableBody')} accepts zero or more tr elements."
            ),
        ),
        b("Valid Usage (Passes Type Checking)"),
        CodeBlock(
            """
            Table(
                TableHead(tr(...)),  # Table head with a single row
                TableBody(tr(...), tr(...))  # Table body with multiple rows
            )
            """,
            language="python",
        ),
        b("Key Benefits"),
        List(
            Item(
                t"{i('Enforce Structure')}: Prevent incorrect usage that could break "
                t"your component's layout or functionality."
            ),
            Item(
                t"{i('Type Safety')}: Static type checkers ensure you're building "
                t"valid component hierarchies."
            ),
        ),
        H2("Attributes"),
        Paragraph(
            t"To ensure type safety and clarity, define your component attributes "
            t"using a subclass of the {Code('Attrs')} class. Here's how:"
        ),
        CodeBlock(
            """
            from typing import NotRequired
            from ludic.attrs import Attrs

            class PersonAttrs(Attrs):
                id: str
                name: str
                is_active: NotRequired[bool]
            """,
            language="python",
        ),
        b(t"Understanding {Code('Attrs')} and {Code('TypedDict')}"),
        List(
            Item(
                t"The {Code('Attrs')} class is built upon Python's {Code('TypedDict')} "
                t"concept (see {
                    Link('PEP-589', to='https://peps.python.org/pep-0589/')
                }) for details). This provides type hints for dictionary-like data "
                t"structures."
            ),
        ),
        H3("Controlling Required Attributes"),
        Paragraph(
            t"In the above case, all attributes except for {{Code('is_active')}} are "
            t"required. If you want to make all attributes NOT required by default, "
            t"you can pass the {Code('total=False')} keyword argument to the class "
            t"definition:"
        ),
        CodeBlock(
            """
            from typing import Required
            from ludic.attrs import Attrs

            class PersonAttrs(Attrs, total=False):
                id: Required[str]
                name: str
                is_active: bool
            """,
            language="python",
        ),
        Paragraph(
            t"In this case, all attributes are optional except for the {Code('id')} "
            t"attribute."
        ),
        Message(
            Title(
                t"The {Code('Attrs')} declaration is an information for type checkers"
            ),
            t"The {Code('Attrs')} class just provides typing information for static "
            t"type checkers. Your code will work even if you pass key-word arguments "
            t"to components without declaring them first.",
        ),
        Paragraph(
            t"All attributes can also subclass from other classes, for example, you "
            t"can extend the attributes for the {Code('<button>')} HTML element:"
        ),
        CodeBlock(
            """
            from ludic.html import TdAttrs
            from ludic.attrs import Attrs

            class TableCellAttrs(TdAttrs):
                is_numeric: bool
            """,
            language="python",
        ),
        Paragraph(
            t"When implementing the component's {Code('render()')} method, you might "
            t"find the {Code('attrs_for(...)')} helper useful too:"
        ),
        CodeBlock(
            """
            class TableCell(ComponentStrict[str, TableCellAttrs]):
                @override
                def render(self) -> td:
                    return td(self.children[0], **self.attrs_for(td))
            """,
            language="python",
        ),
        Paragraph(
            t"The method passes only the attributes registered for the {Code('<td>')} "
            t"element."
        ),
        H3("Pre-defined Attributes"),
        Paragraph(
            t"The {Code('ludic.attrs')} module contains many attribute definitions "
            t"that you can reuse in your components, here are the most used ones:"
        ),
        List(
            Item(
                t"{Code('HtmlAttrs')} – Global HTML attributes available in all "
                t"elements",
                List(
                    Item(
                        t"The {Code('class')} and {Code('for')} attributes have the "
                        t"aliases {Code('class_')} and {Code('for_')}"
                    )
                ),
            ),
            Item(
                t"{Code('EventAttrs')} – Event HTML attributes like "
                t"{Code('on_click')}, {Code('on_key')}, and so on."
            ),
            Item(
                t"{Code('HtmxAttrs')} – All {
                    Link('HTMX attributes', to='https://htmx.org/reference/')
                } available.",
                List(
                    Item(
                        t"All HTMX attributes have aliases with an underscore, e.g. "
                        t"{Code('hx_target')}"
                    )
                ),
            ),
            Item(
                t"{Code('GlobalAttrs')} subclasses {Code('HtmlAttrs')}, "
                t"{Code('EventAttrs')}, and {Code('HtmxAttrs')}"
            ),
            Item(
                t"{Code('[HtmlElementName]Attrs')} – e.g. {Code('ButtonAttrs')}, "
                t"{Code('TdAttrs')}, and so on."
            ),
        ),
        H2("HTML Elements"),
        Paragraph(
            t"All available HTML elements can be found in the {Code('ludic.html')} "
            t"module. The corresponding attributes are located in the {
                Code('ludic.attrs')
            } module."
        ),
        H3("Rendering"),
        Paragraph(
            t"To check how an element or component instance renders in HTML, you can "
            t"use the {Code('.to_html()')} method:"
        ),
        CodeBlock(
            """
            p("click ", Link("here", to="https://example.com")).to_html()
            '<p>click <a href="https://example.com">here</a></p>'
            """,
            language="python",
        ),
        Paragraph("Any string is automatically HTML escaped:"),
        CodeBlock(
            """
            p("<script>alert('Hello world')</script>").to_html()
            "<p>&lt;script&gt;alert('Hello world')&lt;/script&gt;</p>"
            """,
            language="python",
        ),
        H3("Dataset Attributes"),
        Paragraph(
            t"Ludic supports HTML {Code('data-*')} attributes through the special "
            t"{Code('dataset')} attribute. This feature allows you to add custom data "
            t"attributes to HTML elements in a type-safe way."
        ),
        CodeBlock(
            """
            from ludic.html import div

            # Using dataset attribute
            element = div("Content", dataset={"user-id": "123", "category": "primary"})

            # Renders as:
            # <div data-user-id="123" data-category="primary">Content</div>
            """,
            language="python",
        ),
        b("Key Features:"),
        List(
            Item(
                t"{i('Automatic conversion')}: The {Code('dataset')} dictionary keys "
                t"are automatically prefixed with {Code('data-')} in the HTML output."
            ),
            Item(
                t"{i('Hyphen handling')}: Underscores in dataset keys are converted to "
                t"hyphens in HTML: {Code('user_id')} becomes {Code('data-user-id')}."
            ),
            Item(
                t"{i('Type safety')}: Values are automatically converted to strings "
                t"and properly escaped for HTML."
            ),
        ),
        b("Common Use Cases:"),
        List(
            Item("JavaScript integration: storing data for client-side scripts"),
            Item("CSS styling: using data attributes as selectors"),
            Item("HTMX integration: passing data for dynamic behavior"),
            Item("Testing: adding data attributes for test selectors"),
        ),
        CodeBlock(
            """
            # Example with HTMX
            button(
                "Delete Item",
                hx_delete="/api/items",
                dataset={"item-id": "456", "confirm": "Are you sure?"}
            )
            # <button
            #   hx-delete="/api/items"
            #   data-item-id="456"
            #   data-confirm="Are you sure?">Delete Item</button>
            """,
            language="python",
        ),
        H3("Using t-strings"),
        Paragraph(
            t"In Ludic, t-strings offer a bit more readable way to construct component "
            t"content, especially if you need to do a lot of formatting with "
            t"{Code('<b>')}, {Code('<i>')}, and other elements for improving "
            t"typography. Let's modify the previous example using t-strings:"
        ),
        CodeBlock(
            """
            p1 = p(t"click {Link("here", to="https://example.com")}")
            p2 = p("click ", Link("here", to="https://example.com"))

            assert p1 == p2  # Identical components
            """,
            language="python",
        ),
        Paragraph(
            "A t-string keeps its interpolated values as objects. Elements stay "
            "elements, and any other value is escaped like a regular string:"
        ),
        CodeBlock(
            """
            name = "<script>alert(1)</script>"

            p(t"Hello {name}, welcome {b("back")}!").to_html()
            '<p>Hello &lt;script&gt;alert(1)&lt;/script&gt;, welcome <b>back</b>!</p>'
            """,
            language="python",
        ),
        MessageWarning(
            Title("Use t-strings, not f-strings"),
            "An f-string turns an element into text before Ludic can see it, so the "
            "markup ends up escaped on the page.",
        ),
        CodeBlock(
            """
            p(f"click {b("here")}").to_html()
            '<p>click &lt;b&gt;here&lt;/b&gt;</p>'
            """,
            language="python",
        ),
        Message(
            Title("Ludic 0.5.x"),
            t"Ludic 0.5.x for Python 3.12 and 3.13 uses f-strings for the same "
            t"purpose. They keep the elements in a temporary dictionary, which is "
            t"cleared automatically in request handlers of the Ludic Web Framework. "
            t"Anywhere else, wrap the code in {Code('with BaseElement.formatter:')} "
            t"to avoid leaking memory. None of this applies to t-strings.",
        ),
        H2("Available Methods"),
        Paragraph(
            t"All components (and elements too) inherit the following properties and "
            t"methods from the {Code('BaseElement')} class:"
        ),
        List(
            Item(
                t"{Code('BaseElement')}",
                List(
                    Item(t"{Code('children')} – children of the component"),
                    Item(t"{Code('attrs')} – a dictionary containing attributes"),
                    Item(
                        t"{Code('to_html()')} – converts the component to an HTML "
                        t"document"
                    ),
                    Item(
                        t"{Code('to_string()')} – converts the component to a string "
                        t"representation of the tree"
                    ),
                    Item(
                        t"{Code('attrs_for(...)')} – filter attributes to return only "
                        t"those valid for a given element or component"
                    ),
                    Item(
                        t"{Code('has_attributes()')} – whether the component has any "
                        t"attributes"
                    ),
                    Item(
                        t"{Code('is_simple()')} – whether the component contains one "
                        t"primitive child"
                    ),
                    Item(
                        t"{Code('render()')} (*abstract method*) – render the component"
                    ),
                ),
            ),
        ),
        H2("Types and Helpers"),
        Paragraph(
            "The following is a list of all the other parts that can be used to type "
            "and build your application."
        ),
        H4(t"{Code('ludic.elements')}"),
        List(
            Item(t"{Code('Element')} – base for HTML elements"),
            Item(t"{Code('ElementStrict')} – base for strict HTML elements"),
            Item(
                t"{Code('Blank')} – represents a blank component which is not "
                t"rendered, only its children"
            ),
        ),
        H4(t"{Code('ludic.components')}"),
        List(
            Item(t"{Code('Component')} – abstract class for components"),
            Item(t"{Code('ComponentStrict')} – abstract class for strict components"),
            Item(t"{Code('Block')} – component rendering as a div"),
            Item(t"{Code('Inline')} – component rendering as a span"),
        ),
        H4(t"{Code('ludic.types')}"),
        List(
            Item(t"{Code('NoChildren')} – Makes a component accept no children"),
            Item(
                t"{Code('PrimitiveChildren')} – Makes a component accept only "
                t"{Code('str')}, {Code('int')}, {Code('float')} or {Code('bool')}"
            ),
            Item(
                t"{Code('ComplexChildren')} – Makes a component accept only "
                t"non-primitive types"
            ),
            Item(
                t"{Code('AnyChildren')} – Makes a component accept any children types"
            ),
            Item(t"{Code('TAttrs')} – type variable for attributes"),
            Item(t"{Code('TChildren')} – type variable for children of components"),
            Item(
                t"{Code('TChildrenArgs')} – type variable for children of strict "
                t"components"
            ),
            Item(t"{Code('Attrs')} – base for attributes"),
            Item(t"{Code('Safe')} – marker for a safe string which is not escaped"),
            Item(
                t"{Code('JavaScript')} – a marker for javascript, subclasses "
                t"{Code('Safe')}"
            ),
        ),
        H4(t"{Code('ludic.styles')}"),
        List(
            Item(
                t"{Code('GlobalStyles')} – type for HTML classes and their CSS "
                t"properties"
            ),
            Item(t"{Code('CSSProperties')} – type for CSS properties only"),
        ),
        request=request,
        active_item="components",
        title="Ludic - Components",
    )
