from ludic.styles import themes
from ludic.styles.types import Size, SizeClamp
from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    String,
    Whitespace,
)


class LudicStyle(Style):
    name = "ludic-style"

    styles = {
        Whitespace: "#bbbbbb",
        Comment: "#888",
        Comment.Preproc: "#579",
        Comment.Special: "bold #cc0000",
        Keyword: "bold #080",
        Keyword.Pseudo: "#038",
        Keyword.Type: "#339",
        Operator: "#333",
        Operator.Word: "bold #000",
        Name.Builtin: "#007020",
        Name.Function: "bold #06B",
        Name.Class: "bold #B06",
        Name.Namespace: "bold #0e84b5",
        Name.Exception: "bold #F00",
        Name.Variable: "#963",
        Name.Variable.Instance: "#33B",
        Name.Variable.Class: "#369",
        Name.Variable.Global: "bold #d70",
        Name.Constant: "bold #036",
        Name.Label: "bold #970",
        Name.Entity: "bold #800",
        Name.Attribute: "#00C",
        Name.Tag: "#070",
        Name.Decorator: "bold #555",
        String: "#BA2121",
        String.Doc: "italic",
        String.Interpol: "bold #A45A77",
        String.Escape: "bold #AA5D1F",
        String.Regex: "#A45A77",
        String.Symbol: "#B8860B",
        String.Symbol: "#19177C",
        String.Other: "#008000",
        Number: "bold #60E",
        Number.Integer: "bold #00D",
        Number.Float: "bold #60E",
        Number.Hex: "bold #058",
        Number.Oct: "bold #40E",
        Generic.Heading: "bold #000080",
        Generic.Subheading: "bold #800080",
        Generic.Deleted: "#A00000",
        Generic.Inserted: "#00A000",
        Generic.Error: "#FF0000",
        Generic.Emph: "italic",
        Generic.Strong: "bold",
        Generic.EmphStrong: "bold italic",
        Generic.Prompt: "bold #c65d09",
        Generic.Output: "#888",
        Generic.Traceback: "#04D",
        Error: "#F00 bg:#FAA",
    }


theme = themes.LightTheme(
    measure=Size(120, "ch"),
    fonts=themes.Fonts(size=Size(1.01, "em")),
    headers=themes.Headers(
        h1=themes.Header(size=SizeClamp(2.2, 2, 3.6), anchor=False),
        h2=themes.Header(size=SizeClamp(1.8, 1.7, 3), anchor=True),
        h3=themes.Header(size=SizeClamp(1.5, 1.4, 2.5), anchor=True),
        h4=themes.Header(size=SizeClamp(1.3, 1.2, 2.2), anchor=True),
    ),
    layouts=themes.Layouts(
        grid=themes.Grid(cell_size=Size(200, "px")),
        sidebar=themes.Sidebar(side_width=Size(15, "rem")),
        cover=themes.Cover(element="div.cover-main"),
    ),
    code=themes.CodeBlock(style=LudicStyle),
)
