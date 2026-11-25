"""The light and the dark theme of the site.

Both are plain Ludic themes. The page renders the styles of every component
twice, once with each theme, and the dark styles apply when the visitor's
system is in dark mode or when they pick it with the toggle in the header.

Code blocks are highlighted with inline colors, which cannot follow the theme,
so they are dark in both themes, colored by ``CodeStyle``.
"""

from dataclasses import dataclass, field

from ludic.styles import themes
from ludic.styles.types import Color, ColorRange, Size, SizeClamp
from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Token,
)

FONT_SANS = (
    'Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, '
    '"Helvetica Neue", Arial, sans-serif'
)
FONT_MONO = (
    '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, '
    '"Liberation Mono", monospace'
)

FONTS = themes.Fonts(
    primary=FONT_SANS,
    secondary=FONT_SANS,
    monospace=FONT_MONO,
    size=Size(1, "em"),
)

HEADERS = themes.Headers(
    h1=themes.Header(size=SizeClamp(2.1, 1.6, 3), anchor=False),
    h2=themes.Header(size=SizeClamp(1.5, 0.8, 1.9), anchor=True),
    h3=themes.Header(size=SizeClamp(1.2, 0.4, 1.4), anchor=True),
    h4=themes.Header(size=SizeClamp(1.05, 0.2, 1.15), anchor=True),
)

LAYOUTS = themes.Layouts(
    grid=themes.Grid(cell_size=Size(16, "rem")),
    sidebar=themes.Sidebar(side_width=Size(15, "rem")),
    cover=themes.Cover(element="div.cover-main"),
)

ROUNDING = themes.Rounding(less=Size(0.375), normal=Size(0.5), more=Size(0.75))

CODE_TEXT = "#e6edf3"
CODE_MUTED = "#94a3b8"
CODE_COMMENT = "#7d8590"
CODE_KEYWORD = "#c4b5fd"
CODE_STRING = "#5eead4"
CODE_FUNCTION = "#93c5fd"
CODE_BUILTIN = "#7dd3fc"
CODE_CONSTANT = "#fdba74"
CODE_CLASS = "#fcd34d"


class CodeStyle(Style):
    """Syntax colors for the dark code blocks, matching the teal of the site.

    Module names stay in the text color, so an import line reads as two
    keywords around plain names.
    """

    name = "ludic-web"
    styles = {
        Token: CODE_TEXT,
        Comment: f"italic {CODE_COMMENT}",
        Keyword: CODE_KEYWORD,
        Keyword.Constant: CODE_CONSTANT,
        Operator: CODE_MUTED,
        Operator.Word: CODE_KEYWORD,
        Punctuation: CODE_MUTED,
        Name: CODE_TEXT,
        Name.Builtin: CODE_BUILTIN,
        Name.Builtin.Pseudo: "#fda4af",
        Name.Function: CODE_FUNCTION,
        Name.Class: CODE_CLASS,
        Name.Decorator: CODE_CLASS,
        Name.Exception: CODE_CLASS,
        Name.Tag: CODE_BUILTIN,
        Name.Attribute: CODE_CLASS,
        String: CODE_STRING,
        String.Affix: CODE_KEYWORD,
        String.Doc: f"italic {CODE_COMMENT}",
        String.Interpol: CODE_CONSTANT,
        String.Escape: CODE_CONSTANT,
        Number: CODE_CONSTANT,
        Generic.Prompt: CODE_COMMENT,
        Generic.Output: CODE_MUTED,
        Generic.Inserted: "#86efac",
        Generic.Deleted: "#fca5a5",
        Error: "#f87171",
    }


@dataclass
class LudicWebLight(themes.LightTheme):
    name: str = "ludic-web-light"
    measure: Size = Size(72, "ch")
    line_height: float = 1.65
    fonts: themes.Fonts = field(default_factory=lambda: FONTS)
    headers: themes.Headers = field(default_factory=lambda: HEADERS)
    layouts: themes.Layouts = field(default_factory=lambda: LAYOUTS)
    rounding: themes.Rounding = field(default_factory=lambda: ROUNDING)
    colors: themes.Colors = field(
        default_factory=lambda: themes.Colors(
            primary=ColorRange(["#0b5f59", "#0f766e", "#ccfbf1"]),
            secondary=ColorRange(["#1e293b", "#334155", "#e2e8f0"]),
            success=ColorRange(["#14532d", "#15803d", "#dcfce7"]),
            info=ColorRange(["#0c4a6e", "#0369a1", "#e0f2fe"]),
            warning=ColorRange(["#78350f", "#b45309", "#fef3c7"]),
            danger=ColorRange(["#7f1d1d", "#b91c1c", "#fee2e2"]),
            light=ColorRange(["#cbd5e1", "#e2e8f0", "#f1f5f9", "#f8fafc"]),
            dark=ColorRange(["#020617", "#0f172a", "#1e293b", "#475569", "#64748b"]),
            white=Color("#ffffff"),
            black=Color("#0f172a"),
        )
    )
    code: themes.CodeBlock = field(
        default_factory=lambda: themes.CodeBlock(
            color=Color(CODE_TEXT),
            background_color=Color("#0d1117"),
            line_number_color=Color("#7d8590"),
            line_numbers=False,
            font_size=Size(0.875),
            style=CodeStyle,
        )
    )


@dataclass
class LudicWebDark(themes.DarkTheme):
    name: str = "ludic-web-dark"
    measure: Size = Size(72, "ch")
    line_height: float = 1.65
    fonts: themes.Fonts = field(default_factory=lambda: FONTS)
    headers: themes.Headers = field(default_factory=lambda: HEADERS)
    layouts: themes.Layouts = field(default_factory=lambda: LAYOUTS)
    rounding: themes.Rounding = field(default_factory=lambda: ROUNDING)
    colors: themes.Colors = field(
        default_factory=lambda: themes.Colors(
            primary=ColorRange(["#5eead4", "#2dd4bf", "#134e4a"]),
            secondary=ColorRange(["#e2e8f0", "#94a3b8", "#1e293b"]),
            success=ColorRange(["#86efac", "#4ade80", "#14532d"]),
            info=ColorRange(["#7dd3fc", "#38bdf8", "#0c4a6e"]),
            warning=ColorRange(["#fcd34d", "#fbbf24", "#78350f"]),
            danger=ColorRange(["#fca5a5", "#f87171", "#7f1d1d"]),
            light=ColorRange(["#334155", "#243041", "#151d2b", "#10172a"]),
            dark=ColorRange(["#f8fafc", "#e2e8f0", "#cbd5e1", "#94a3b8", "#7c8ba1"]),
            white=Color("#0b1018"),
            black=Color("#f8fafc"),
        )
    )
    code: themes.CodeBlock = field(
        default_factory=lambda: themes.CodeBlock(
            color=Color(CODE_TEXT),
            background_color=Color("#131c2b"),
            line_number_color=Color("#7d8590"),
            line_numbers=False,
            font_size=Size(0.875),
            style=CodeStyle,
        )
    )


light_theme = LudicWebLight()
dark_theme = LudicWebDark()
