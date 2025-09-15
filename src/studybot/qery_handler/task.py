from telegram import CallbackQuery, Update

from studybot.config import config
from studybot.database import db


async def task(
    update: Update,
    query: CallbackQuery,
) -> None:
    if update.effective_user is None:
        return
    user_id = update.effective_user.id
    data = await db.get_user_db(user_id)
    if query.data is None:
        return
    task = query.data[len(config.TASK_START_QERY) :]
    user_data = await data
    subject = user_data[config.SUBJECTS]
    number = user_data[config.NUMBER]
    user_data[config.TASK] = task
    real_task = await db.get_task(subject=subject, number=number, task_id=task)
    user_data[config.TASK_TEXT] = task_text = real_task[config.TASK_TEXT]
    user_data[config.TASK_ANSWER] = real_task[config.TASK_ANSWER]

    await query.edit_message_text(
        text=config.ANSWER_QESTION_TEXT.format(
            subject,
            number,
            task,
            task_text,
        ),
    )
    await db.update_user_data(user_id, user_data)
