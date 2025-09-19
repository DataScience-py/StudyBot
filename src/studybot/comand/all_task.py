from telegram import Update
from telegram.ext import ContextTypes

from studybot.config import config, get_logger, time_logger
from studybot.database import db
from studybot.utils.markup import create_markup

logger = get_logger(__name__)


@time_logger(logger)
async def all_tasks(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> None:
    if update.effective_user is None:
        return
    data = await db.get_user_db(user_id=update.effective_user.id)
    subjects = await db.get_subjects()
    if update.message is None:
        return
    markup = create_markup(
        objects=subjects,
        row_len=1,
        first_callback=config.SUBJECTS_START_QERY,
    )
    await update.message.reply_text(
        text=config.CHOICE_SUBJECTS_TEXT,
        reply_markup=markup,
    )
    user_data = await data

    user_data[config.ATTEMPTS] = 0

    await db.update_user_data(
        update.effective_user.id,
        user_data,
    )
