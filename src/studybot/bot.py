"""Create bot."""

import asyncio
from typing import Any

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
)

from .comand import start
from .config import config, get_logger
from .database import db
from .database.database import clear_user_ram_time

logger = get_logger()


def add_handlers(app: Application[Any, Any, Any, Any, Any, Any]) -> None:
    """Add handler to bot."""
    app.add_handler(CommandHandler("start", start))


async def on_shutdown(app: Application[Any, Any, Any, Any, Any, Any]) -> None:  # noqa: ARG001
    logger.info("Saving all RAM data before shutdown...")
    await db.save_all_user_data()


async def task_run() -> None:
    task = asyncio.create_task(clear_user_ram_time())


async def run() -> None:
    """Run study bot."""
    config.RUN = True
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    add_handlers(app)

    task = asyncio.create_task(task_run())

    logger.info("StudyBot start databse")
    logger.info("Study bot started")
    app.post_shutdown = on_shutdown
    app.run_polling(close_loop=False)
    await task
    config.RUN = False
