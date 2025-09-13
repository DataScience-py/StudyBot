"""Create bot."""

from telegram.ext import (
    ApplicationBuilder,
)

from .config import Config


def run() -> None:
    """Run study bot."""
    config = Config()
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    app.run_polling()
