from pathlib import Path

import aiofiles
from telegram import CallbackQuery, InputMediaPhoto, Update

from studybot.config import config, get_logger
from studybot.database import db

logger = get_logger(__name__)


async def task(
    update: Update,
    query: CallbackQuery,
) -> None:
    if update.effective_user is None:
        return
    if update.effective_chat is None:
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
    task_data = await db.get_task(subject=subject, number=number, task_id=task)
    user_data[config.TASK_TEXT] = task_text = task_data[config.TASK_TEXT]
    user_data[config.TASK_ANSWER] = task_data[config.TASK_ANSWER]

    text = config.ANSWER_QESTION_TEXT.format(
        subject,
        number,
        task,
        task_text,
    )
    await query.edit_message_text(
        text=text,
    )

    if config.TASK_IMG in task_data:
        media = []
        for img_path in task_data[config.TASK_IMG]:
            if Path(img_path).exists():
                async with aiofiles.open(img_path, "rb") as img_file:
                    file_content = await img_file.read()
                    media.append(InputMediaPhoto(media=file_content))
            else:
                logger.warning("Файл не найден: %s", img_path)
        if media:
            await update.effective_chat.send_media_group(media=media)

    await db.update_user_data(user_id, user_data)
