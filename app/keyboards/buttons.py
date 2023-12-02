from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_menu_default():
    buttons = [
        InlineKeyboardButton(text="Остаток", callback_data="button_summ"),
        InlineKeyboardButton(text="Список затрат", callback_data="button_expenses"),
        InlineKeyboardButton(text="Должники", callback_data="button_borrowed_"),
    ]
    return keyboard_builder(buttons)


def keyboard_builder(buttons: List):
    builder = InlineKeyboardBuilder()
    builder.add(*buttons)

    return builder.as_markup()
