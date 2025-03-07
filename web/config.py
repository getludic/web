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
