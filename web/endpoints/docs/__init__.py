from ludic.web.routing import Router

from . import (
    components,
    getting_started,
    htmx,
    index,
    integrations,
    styles,
    web_framework,
)

router = Router()

router.add_route("/", index.index)
router.add_route("/counter/{number:int}", index.Counter)
router.add_route("/components", components.components)
router.add_route("/getting-started", getting_started.getting_started)
router.add_route("/htmx", htmx.htmx)
router.add_route("/htmx/example", htmx.htmx_example)
router.add_route("/htmx/content", htmx.htmx_content)
router.add_route("/styles", styles.styles)
router.add_route("/web-framework", web_framework.web_framework)
router.add_route("/integrations", integrations.integrations)
