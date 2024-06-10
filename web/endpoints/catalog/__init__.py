from ludic.web.routing import Router

from . import buttons, forms, index, layouts, loaders, messages, tables, typography

router = Router()

router.add_route("/", index.index)
router.add_route("/buttons", buttons.buttons)
router.add_route("/forms", forms.forms)
router.add_route("/tables", tables.tables)
router.add_route("/layouts", layouts.layouts)
router.add_route("/messages", messages.messages)
router.add_route("/loaders", loaders.loaders)
router.add_route("/typography", typography.typography)
