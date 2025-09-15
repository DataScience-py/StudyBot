from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, ContextTypes

from studybot.config import config

from .numbers import all_numbers
from .task import task
from .tasks import all_task


async def handle_callback_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """handle_callback_query handle callback query."""
    if update.callback_query is None:
        return
    query = update.callback_query
    if query is not None:
        await query.answer()
        if query.data is None:
            return
        if query.data.startswith(config.SUBJECTS_START_QERY):
            await all_numbers(update, query)
        if query.data.startswith(config.NUMBER_START_QERY):
            await all_task(update, query)
        if query.data.startswith(config.TASK_START_QERY):
            await task(update, query)
