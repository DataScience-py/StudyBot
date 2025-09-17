from telegram import Update
from telegram.ext import ContextTypes

from studybot.config import config
from studybot.database import db


async def check_task_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.effective_user is None:
        return
    user_id = update.effective_user.id
    data = await db.get_user_db(user_id)
    if update.message is None:
        return
    if update.message.text is None:
        return
    user_answer = update.message.text.lower()
    user_data = await data

    if config.TASK_ANSWER in user_data:
        last_answer = user_data[config.TASK_ANSWER]
    else:
        subject = user_data.get(config.SUBJECTS)
        number = user_data.get(config.NUMBER)
        task = user_data.get(config.TASK)
        if subject is None or number is None or task is None:
            await update.message.reply_text(
                "Выберите сначала задание. Используйте /tasks!",
            )
            return
        task = await db.get_task(subject=subject, number=number, task_id=task)
        user_data[config.TASK_TEXT] = task[config.TASK_TEXT]
        user_data[config.TASK_ANSWER] = last_answer = task[config.TASK_ANSWER]
    if user_answer == last_answer:
        del user_data[config.TASK_ANSWER]
        del user_data[config.TASK_TEXT]
        await update.message.reply_text("Верно!")
    else:
        await update.message.reply_text("Не верно!")

    await db.update_user_data(user_id, user_data)
