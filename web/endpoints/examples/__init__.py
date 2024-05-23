from ludic.web.routing import Router

from . import (
    bulk_update,
    click_to_edit,
    click_to_load,
    delete_row,
    edit_row,
    index,
    infinite_scroll,
    lazy_loading,
)

router = Router()

router.add_route("/", index.index)
router.add_route("/bulk-update", bulk_update.bulk_update)
router.add_route("/click-to-edit", click_to_edit.click_to_edit)
router.add_route("/click-to-load", click_to_load.click_to_load)
router.add_route("/delete-row", delete_row.delete_row)
router.add_route("/edit-row", edit_row.edit_row)
router.add_route("/infinite-scroll", infinite_scroll.infinite_scroll)
router.add_route("/lazy-loading", lazy_loading.lazy_loading)
