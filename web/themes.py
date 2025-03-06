from ludic.styles import themes
from ludic.styles.types import Size, SizeClamp

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
)
