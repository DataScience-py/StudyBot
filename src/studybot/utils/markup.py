from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def create_markup(
    objects: list[str],
    row_len: int = 8,
    first_callback: str = "",
) -> InlineKeyboardMarkup:
    """Generate keyboard for callback query."""
    keyboard = []
    row = []
    for item in objects:
        row.append(
            InlineKeyboardButton(item, callback_data=first_callback + item),
        )
        if len(row) == row_len:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)
