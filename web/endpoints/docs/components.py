from ludic.catalog.headers import H1, H2, H3, H4
from ludic.catalog.lists import Item, List, NumberedList
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
                f"{b("Components")}: a component is a reusable chunk of code that "
                "defines a piece of your user interface. Think of it like a blueprint "
                "for an HTML element, but more powerful."
            ),
            Item(
                f"{b("Elements")}: these represent the individual HTML tags (like "
                f"{Code("<a>")}, {Code("<div>")}, {Code("<h1>")}, etc.) that make up "
                "the structure of your page."
            ),
            Item(
                f"{b("Attributes")}: These help define the properties on your "
                "components and elements. They let you modify things like a link's "
                "destination, text color, or an element's size."
            ),
            Item(
                f"{b("Hierarchy")}: Components can contain other components or "
                "elements, creating a tree-like structure."
            ),
            Item(
                f"{b("Types")}: A safety net to help you write correct code, "
                "preventing errors just like making sure LEGO pieces fit together "
                "properly."
            ),
        ),
        H2("Types of Components"),
        List(
            Item(
                f"{b("Regular")}: These are flexible, letting you have multiple "
                "children of any type."
            ),
            Item(
                f"{b("Strict")}: Perfect for when you need precise control over the "
                "structure of your component – like a table where you must have a head "
                "and a body."
            ),
        ),
        H2("Regular Components"),
        Paragraph(
            f"Let's break down a simplified version of the {Code("Link")} component:"
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
                f"{i("HTML Rendering")}: This component renders as the following HTML "
                f"element:",
                List(Item(Code('<a href="..." style="color:#abc">...</a>'))),
            ),
            Item(
                f"{i("Type Hints")}: {Code("Component[str, LinkAttrs]")} provides type "
                f"safety:",
                List(
                    Item(
                        f"{i("str")}: Enforces that all children of the component "
                        "must be strings"
                    ),
                    Item(
                        f"{i("LinkAttrs")}: Ensures the required to attribute is "
                        "present"
                    ),
                ),
            ),
            Item(
                f"{i("Attributes")}: {Code("LinkAttrs")} inherits from "
                f"{Code("Attrs")}, which is a {Code("TypedDict")} "
                f"(a dictionary with defined types for its keys)",
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
            "The current definition doesn't strictly enforce a single child. "
            "This means you could technically pass multiple strings "
            f"({Code('Link("a", "b")')}). To create a stricter component, inherit "
            f"from {Code("ComponentStrict")}: This subclass of Component allows for "
            "finer control over children. More about this in the next section."
        ),
        H2("Strict Components"),
        Paragraph(
            "Strict components offer more precise control over the types and "
            "structures of their children compared to regular components. Let's "
            f"illustrate this with a simplified {Code("Table")} component:"
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
                f"{i("Strictness")}: The {Code("ComponentStrict")} class allows you to "
                "enforce the exact types and order of children."
            ),
            Item(
                f"{i("Table Structure")}:",
                List(
                    Item(
                        f"{Code("Table")}: Expects precisely two children: a "
                        f"{Code("TableHead")} followed by a {Code("TableBody")}."
                    ),
                    Item(
                        f"{Code("TableHead")}: Accepts only a single {Code("tr")} "
                        "(table row) element as its child."
                    ),
                    Item(
                        f"{Code("TableBody")}: Accepts a variable number of "
                        f"{Code("tr")} elements as children."
                    ),
                ),
            ),
            Item(
                f"{i("Type Hints")}: The {Code("*tuple[tr, ...]")} syntax indicates "
                f"that {Code("TableBody")} accepts zero or more tr elements."
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
                f"{i("Enforce Structure")}: Prevent incorrect usage that could break "
                "your component's layout or functionality."
            ),
            Item(
                f"{i("Type Safety")}: Static type checkers ensure you're building "
                "valid component hierarchies."
            ),
        ),
        H2("Attributes"),
        Paragraph(
            "To ensure type safety and clarity, define your component attributes using "
            f"a subclass of the {Code("Attrs")} class. Here's how:"
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
        b(f"Understanding {Code("Attrs")} and {Code("TypedDict")}"),
        List(
            Item(
                f"The {Code("Attrs")} class is built upon Python's {Code("TypedDict")} "
                f"concept (see {Link(
                    "PEP-589", to="https://peps.python.org/pep-0589/"
                )}) for details). This provides type hints for dictionary-like data "
                "structures."
            ),
        ),
        H3("Controlling Required Attributes"),
        Paragraph(
            "In the above case, all attributes except for {Code('is_active')} are "
            "required. If you want to make all attributes NOT required by default, "
            f"you can pass the {Code("total=False")} keyword argument to the class "
            "definition:"
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
            f"In this case, all attributes are optional except for the {Code("id")} "
            "attribute."
        ),
        Message(
            Title(
                f"The {Code("Attrs")} declaration is an information for type checkers"
            ),
            f"The {Code("Attrs")} class just provides typing information for static "
            "type checkers. Your code will work even if you pass key-word arguments to "
            "components without declaring them first.",
        ),
        Paragraph(
            "All attributes can also subclass from other classes, for example, you can "
            f"extend the attributes for the {Code("<button>")} HTML element:"
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
            f"When implementing the component's {Code("render()")} method, you might "
            f"find the {Code("attrs_for(...)")} helper useful too:"
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
            f"The method passes only the attributes registered for the {Code("<td>")} "
            "element."
        ),
        H3("Pre-defined Attributes"),
        Paragraph(
            f"The {Code("ludic.attrs")} module contains many attribute definitions "
            "that you can reuse in your components, here are the most used ones:"
        ),
        List(
            Item(
                f"{Code("HtmlAttrs")} – Global HTML attributes available in all "
                "elements",
                List(
                    Item(
                        f"The {Code("class")} and {Code("for")} attributes have the "
                        f"aliases {Code("class_")} and {Code("for_")}"
                    )
                ),
            ),
            Item(
                f"{Code("EventAttrs")} – Event HTML attributes like "
                f"{Code("on_click")}, {Code("on_key")}, and so on."
            ),
            Item(
                f"{Code("HtmxAttrs")} – All {Link(
                    "HTMX attributes", to="https://htmx.org/reference/"
                )} available.",
                List(
                    Item(
                        "All HTMX attributes have aliases with an underscore, e.g. "
                        f"{Code("hx_target")}"
                    )
                ),
            ),
            Item(
                f"{Code("GlobalAttrs")} subclasses {Code("HtmlAttrs")}, "
                f"{Code("EventAttrs")}, and {Code("HtmxAttrs")}"
            ),
            Item(
                f"{Code("[HtmlElementName]Attrs")} – e.g. {Code("ButtonAttrs")}, "
                f"{Code("TdAttrs")}, and so on."
            ),
        ),
        H2("HTML Elements"),
        Paragraph(
            f"All available HTML elements can be found in the {Code("ludic.html")} "
            f"module. The corresponding attributes are located in the {Code(
                "ludic.attrs"
            )} module."
        ),
        H3("Rendering"),
        Paragraph(
            "To check how an element or component instance renders in HTML, you can "
            f"use the {Code(".to_html()")} method:"
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
            '<p>&lt;script&gt;alert(&#x27;Hello world&#x27;)&lt;/script&gt;</p>'
            """,
            language="python",
        ),
        H3("Using f-strings"),
        Paragraph(
            "In Ludic, f-strings offer a bit more readable way to construct component "
            "content, especially if you need to do a lot of formatting with "
            f"{Code("<b>")}, {Code("<i>")}, and other elements for improving "
            "typography. Let's modify the previous example using f-strings:"
        ),
        CodeBlock(
            """
            p1 = p(f"click {Link("here", to="https://example.com")}")
            p2 = p("click ", Link("here", to="https://example.com"))

            assert p1 == p2  # Identical components
            """,
            language="python",
        ),
        b("Important Note: Memory Considerations"),
        Paragraph(
            f"{i("Temporary Dictionaries")}: to make f-strings safely work, they "
            "internally create temporary dictionaries to hold the component "
            "instances. To avoid memory leaks, these dictionaries need to be "
            "consumed by a component."
        ),
        Paragraph("There are two cases it can create hanging objects (memory leaks):"),
        NumberedList(
            Item("Component initialization with the f-string fails."),
            Item(
                "You store an f-string in a variable but don't pass it to a "
                "component."
            ),
        ),
        MessageWarning(
            Title("Possible memory leak"),
            "The implementation of f-strings requires the creation of a temporary dict "
            "which can result in hanging objects in memory. To avoid memory leaks, "
            f"there is the {Code('BaseElement.formatter')} attribute which is a "
            "context manager clearing the temporary dict on exit.",
        ),
        b(f"The {Code("BaseElement.formatter")} Context Manager"),
        CodeBlock(
            """
            from ludic.base import BaseElement

            with BaseElement.formatter:
                # you can do anything with f-strings here, no memory leak
                # is created since formatter dict is cleared on exit
            """,
            language="python",
        ),
        b("Web Framework Request Handlers"),
        Paragraph(
            "The Ludic Web Framework (built on Starlette) automatically wraps request "
            f"handlers with {Code("BaseElement.formatter")}, providing a safe "
            "environment for f-strings.",
        ),
        b("Key Takeaways"),
        Paragraph(
            "While f-strings are convenient, exercise caution to prevent memory leaks. "
            "Use them within the provided safety mechanisms. In contexts like task "
            "queues or other web frameworks, you can use a similar mechanism of "
            "wrapping to achieve memory safety."
        ),
        H2("Available Methods"),
        Paragraph(
            "All components (and elements too) inherit the following properties and "
            f"methods from the {Code("BaseElement")} class:"
        ),
        List(
            Item(
                f"{Code("BaseElement")}",
                List(
                    Item(f"{Code("children")} – children of the component"),
                    Item(f"{Code("attrs")} – a dictionary containing attributes"),
                    Item(
                        f"{Code("to_html()")} – converts the component to an HTML "
                        "document"
                    ),
                    Item(
                        f"{Code("to_string()")} – converts the component to a string "
                        "representation of the tree"
                    ),
                    Item(
                        f"{Code("attrs_for(...)")} – filter attributes to return only "
                        "those valid for a given element or component"
                    ),
                    Item(
                        f"{Code("has_attributes()")} – whether the component has any "
                        "attributes"
                    ),
                    Item(
                        f"{Code("is_simple()")} – whether the component contains one "
                        "primitive child"
                    ),
                    Item(
                        f"{Code("render()")} (*abstract method*) – render the component"
                    ),
                ),
            ),
        ),
        H2("Types and Helpers"),
        Paragraph(
            "The following is a list of all the other parts that can be used to type "
            "and build your application."
        ),
        H4(f"{Code("ludic.elements")}"),
        List(
            Item(f"{Code("Element")} – base for HTML elements"),
            Item(f"{Code("ElementStrict")} – base for strict HTML elements"),
            Item(
                f"{Code("Blank")} – represents a blank component which is not "
                f"rendered, only its children"
            ),
        ),
        H4(f"{Code("ludic.components")}"),
        List(
            Item(f"{Code("Component")} – abstract class for components"),
            Item(f"{Code("ComponentStrict")} – abstract class for strict components"),
            Item(f"{Code("Block")} – component rendering as a div"),
            Item(f"{Code("Inline")} – component rendering as a span"),
        ),
        H4(f"{Code("ludic.types")}"),
        List(
            Item(f"{Code("NoChildren")} – Makes a component accept no children"),
            Item(
                f"{Code("PrimitiveChildren")} – Makes a component accept only "
                f"{Code("str")}, {Code("int")}, {Code("float")} or {Code("bool")}"
            ),
            Item(
                f"{Code("ComplexChildren")} – Makes a component accept only "
                "non-primitive types"
            ),
            Item(
                f"{Code("AnyChildren")} – Makes a component accept any children types"
            ),
            Item(f"{Code("TAttrs")} – type variable for attributes"),
            Item(f"{Code("TChildren")} – type variable for children of components"),
            Item(
                f"{Code("TChildrenArgs")} – type variable for children of strict "
                "components"
            ),
            Item(f"{Code("Attrs")} – base for attributes"),
            Item(f"{Code("Safe")} – marker for a safe string which is not escaped"),
            Item(
                f"{Code("JavaScript")} – a marker for javascript, subclasses "
                f"{Code("Safe")}"
            ),
        ),
        H4(f"{Code("ludic.styles")}"),
        List(
            Item(
                f"{Code("GlobalStyles")} – type for HTML classes and their CSS "
                "properties"
            ),
            Item(f"{Code("CSSProperties")} – type for CSS properties only"),
        ),
        request=request,
        active_item="components",
        title="Ludic - Components",
    )
