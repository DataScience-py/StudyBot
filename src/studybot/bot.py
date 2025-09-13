"""Create bot."""

from telegram.ext import ApplicationBuilder, CommandHandler

from .comand import start
from .config import Config


def run() -> None:
    """Run study bot."""
    config = Config()
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.run_polling()
