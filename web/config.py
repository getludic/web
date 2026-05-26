import os

DEBUG = os.getenv("LUDIC_DEBUG", "0") == "1"

AUTHOR = os.getenv("LUDIC_AUTHOR", "Pavel Dedik")
TITLE = os.getenv("LUDIC_TITLE", "The Ludic Framework")
HOME_URL = os.getenv("LUDIC_HOME_URL", "https://getludic.dev")
GITHUB_REPO_URL = os.getenv(
    "LUDIC_GITHUB_REPO_URL", "https://github.com/getludic/ludic"
)
GITHUB_REPO_WEB_URL = os.getenv(
    "LUDIC_GITHUB_REPO_WEB_URL", "https://github.com/getludic/web"
)
DISCORD_INVITE_URL = os.getenv("DISCORD_INVITE_URL", "https://discord.gg/7nK4zAXAYC")

HTMX_VERSION = os.getenv("LUDIC_HTMX_VERSION", "1.9.12")
ENABLE_PROFILING = os.getenv("LUDIC_ENABLE_PROFILING", "0") == "1"

# Hosts the app will respond to. Anything else gets a 400 from
# TrustedHostMiddleware. Validated AFTER TrustForwardedHostMiddleware
# rewrites Host from X-Forwarded-Host, so this is what stops a request
# to the public Lambda Function URL (AuthType=NONE) from poisoning
# `request.url_for(...)` with a forged X-Forwarded-Host. Direct hits to
# the raw Lambda URL are also rejected because that hostname is not in
# the list.
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        "LUDIC_ALLOWED_HOSTS",
        "getludic.dev,www.getludic.dev,localhost,127.0.0.1,testserver",
    ).split(",")
    if h.strip()
]
