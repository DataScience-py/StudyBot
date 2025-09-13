"""Start/Hello command."""

from telegram import Update
from telegram.ext import ContextTypes

from studybot.config import get_logger, time_logger

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
    if update.message is not None and update.effective_user is not None:
        await update.message.reply_text(
            "Привет, " + update.effective_user.first_name,
        )
