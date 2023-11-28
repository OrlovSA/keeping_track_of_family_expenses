from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_markup():
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="summ", callback_data="summ"),
        InlineKeyboardButton(text="expenses", callback_data="expenses"),
    ]
    builder.add(*buttons)
    return builder.as_markup()
