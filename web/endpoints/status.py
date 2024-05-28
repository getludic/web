from ludic.html import span
from ludic.web import LudicApp

from web import config

app = LudicApp(debug=config.DEBUG)


@app.get("/live")
def liveness() -> span:
    return span("ok", id="status")


@app.get("/ready")
def readiness() -> span:
    return span("ok", id="status")
