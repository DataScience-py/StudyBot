from telegram import Update
from telegram.ext import ContextTypes

from studybot.config import config
from studybot.database import db

from .check_task import check_task_handler
from .task_loader import get_task_message


async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.effective_user is None:
        return
    user_id = update.effective_user.id
    data = await db.get_user_db(user_id)
    user_db = await data
    if user_db.get(config.WAIT_TASK_NUMBER) is not None:
        await get_task_message(update, context, user_db)
    else:
        await check_task_handler(update, context)
