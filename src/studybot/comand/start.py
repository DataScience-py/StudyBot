"""Start/Hello command."""

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
