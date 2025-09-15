"""Start/Hello command."""

from time import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import Task
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from studybot.config import get_logger, time_logger
from studybot.database import db

logger = get_logger(__name__)


@time_logger(logger)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: ARG001
    """
    Start comand for the bot.

    Parameters
    ----------
    update : Update
        message module
    context : ContextTypes.DEFAULT_TYPE
        user information data (save and get)
    """
    if update.effective_user is None:
        logger.warning("User doesn't have effective_user")
        return
    user_id: int = update.effective_user.id
    data: Task[dict[str, Any]] = await db.get_user_db(
        user_id=user_id,
    )

    if update.message is not None and update.effective_user is not None:
        await update.message.reply_text(
            "Привет, " + update.effective_user.first_name,
        )
    user_data: dict[str, Any] = await data
    if user_data.get("Hello_time") is None:
        user_data["Hello_time"] = time()
    await db.update_user_data(user_id, user_data)
