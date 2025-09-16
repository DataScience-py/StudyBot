from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from studybot.config import config
from studybot.database import db


async def get_task_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_db: dict[str, Any],
) -> None:
    del user_db[config.WAIT_TASK_NUMBER]
    if (user_db.get(config.SUBJECTS) is None) or (
        user_db.get(config.NUMBER) is None
    ):
        return
    subject = user_db[config.SUBJECTS]
    number = user_db[config.NUMBER]
    if update.message is None:
        return
    if update.message.text is None:
        return
    if update.effective_user is None:
        return
    task = update.message.text.lower()
    try:
        task_data = await db.get_task(subject, number, task)
    except FileNotFoundError:
        await update.effective_user.send_message(
            text=config.FILE_NOT_FOUND_ERROR.format(task),
        )
        return
    user_db[config.TASK] = task
    user_db[config.TASK_TEXT] = task_data[config.TASK_TEXT]
    user_db[config.TASK_ANSWER] = task_data[config.TASK_ANSWER]
    await update.effective_user.send_message(
        text=config.ANSWER_QESTION_TEXT.format(
            subject,
            number,
            task,
            user_db[config.TASK_TEXT],
        ),
    )
    await db.update_user_data(
        user_id=update.effective_user.id,
        data=user_db,
    )
