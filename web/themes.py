"""The light and the dark theme of the site.

Both are plain Ludic themes. The page renders the styles of every component
twice, once with each theme, and the dark styles apply when the visitor's
system is in dark mode or when they pick it with the toggle in the header.

Code blocks are highlighted with inline colors, which cannot follow the theme,
so they are dark in both themes.
"""

from dataclasses import dataclass, field

from ludic.styles import themes
from ludic.styles.types import Color, ColorRange, Size, SizeClamp

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

CODE_STYLE = "github-dark"


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
            color=Color("#e6edf3"),
            background_color=Color("#0d1117"),
            line_number_color=Color("#7d8590"),
            line_numbers=False,
            font_size=Size(0.875),
            style=CODE_STYLE,
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
            color=Color("#e6edf3"),
            background_color=Color("#131c2b"),
            line_number_color=Color("#7d8590"),
            line_numbers=False,
            font_size=Size(0.875),
            style=CODE_STYLE,
        )
    )


light_theme = LudicWebLight()
dark_theme = LudicWebDark()
