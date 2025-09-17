import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def natural_sort_key(s: str) -> list[str]:
    """
    Создает ключ для естественной сортировки.
    Разбивает строку на последовательности чисел и не-чисел.
    """
    return [int(c) if c.isdigit() else c for c in re.split("([0-9]+)", s)]


def create_markup(
    objects: list[str],
    row_len: int = 8,
    first_callback: str = "",
) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру с естественной сортировкой элементов.
    """
    keyboard = []
    row = []

    # Применяем естественную сортировку
    objects.sort(key=natural_sort_key)

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
