"""Create bot."""

from telegram.ext import ApplicationBuilder, CommandHandler

from .comand import start
from .config import Config, get_logger


def run() -> None:
    """Run study bot."""
    logger = get_logger()
    config = Config()
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    logger.info("Study bot started")
    app.run_polling()
