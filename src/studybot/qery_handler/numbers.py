from telegram import CallbackQuery, Update

from studybot.config import config
from studybot.database import db
from studybot.utils.markup import create_markup


async def all_numbers(update: Update, query: CallbackQuery) -> None:
    if update.effective_user is None:
        return
    user_id = update.effective_user.id
    data = await db.get_user_db(user_id)
    if query.data is None:
        return
    subject = query.data[len(config.SUBJECTS_START_QERY) :]
    numbers = await db.get_numbers(subject=subject)
    markup = create_markup(
        numbers,
        row_len=1,
        first_callback=config.NUMBER_START_QERY,
    )
    await query.edit_message_text(
        text=config.CHOICE_NUMBER_TEXT.format(subject),
        reply_markup=markup,
    )
    user_data = await data
    user_data[config.SUBJECTS] = subject
    await db.update_user_data(user_id, user_data)
