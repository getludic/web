from ludic.web.routing import Mount, Router

from . import bulk_update as bu
from . import click_to_edit as ce
from . import click_to_load as cl
from . import complex_layout as cla
from . import delete_row as dr
from . import edit_row as er
from . import infinite_scroll as isc
from . import lazy_loading as ll

router = Router(
    routes=[
        Mount("/bulk-update/", bu.app, name="bulk_update"),
        Mount("/click-to-edit/", ce.app, name="click_to_edit"),
        Mount("/click-to-load/", cl.app, name="click_to_load"),
        Mount("/complex-layout/", cla.app, name="complex_layout"),
        Mount("/delete-row/", dr.app, name="delete_row"),
        Mount("/edit-row/", er.app, name="edit_row"),
        Mount("/infinite-scroll/", isc.app, name="infinite_scroll"),
        Mount("/lazy-loading/", ll.app, name="lazy_loading"),
    ],
)
