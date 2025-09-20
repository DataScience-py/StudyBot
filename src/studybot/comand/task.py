from telegram import Update
from telegram.ext import ContextTypes

from studybot.config import config
from studybot.database import db
from studybot.utils.markup import create_markup


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user is None:
        return
    data = await db.get_user_db(user_id=update.effective_user.id)
    if update.message is None:
        return
    user_data = await data

    subject = user_data.get(config.SUBJECTS)
    number = user_data.get(config.NUMBER)
    if (subject is None) or (number is None):
        return
    tasks = await db.get_all_task(subject, number)

    markup = create_markup(
        objects=tasks,
        row_len=1,
        first_callback=config.SUBJECTS_START_QERY,
    )
    if len(tasks) <= config.MAX_LEN_TAKS:
        markup = create_markup(tasks, first_callback=config.TASK_START_QERY)
        await update.message.reply_text(
            text=config.CHOICE_TASK_TEXT.format(subject, number),
            reply_markup=markup,
        )
    else:
        user_data[config.WAIT_TASK_NUMBER] = True
        await update.message.reply_text(
            text=config.CHOICE_TASK_TEXT_WRITE.format(
                subject,
                number,
                len(tasks),
            ),
        )

    user_data[config.ATTEMPTS] = 0

    await db.update_user_data(update.effective_user.id, user_data)
