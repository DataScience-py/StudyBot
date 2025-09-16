from telegram import CallbackQuery, Update

from studybot.config import config
from studybot.database import db
from studybot.utils.markup import create_markup


async def all_task(update: Update, query: CallbackQuery) -> None:
    if update.effective_user is None:
        return
    user_id = update.effective_user.id
    data = await db.get_user_db(user_id)
    user_data = await data

    if query.data is None:
        return
    number = query.data[len(config.NUMBER_START_QERY) :]
    user_data[config.NUMBER] = number
    subject = user_data.get(config.SUBJECTS)
    if (subject := user_data.get(config.SUBJECTS)) is None:
        # TODO: Сначала выберите SUBJECT
        return
    tasks = await db.get_all_task(
        subject,
        number,
    )
    if len(tasks) <= config.MAX_LEN_TAKS:
        markup = create_markup(tasks, first_callback=config.TASK_START_QERY)
        await query.edit_message_text(
            text=config.CHOICE_TASK_TEXT.format(subject, number),
            reply_markup=markup,
        )
    else:
        user_data[config.WAIT_TASK_NUMBER] = True
        await query.edit_message_text(
            text=config.CHOICE_TASK_TEXT_WRITE.format(
                subject,
                number,
                len(tasks),
            ),
        )
    await db.update_user_data(user_id, user_data)
