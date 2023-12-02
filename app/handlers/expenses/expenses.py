from typing import List

from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from aiogram.types import Message

from app.database.models.expenses import Expenses
from app.database.models.money import Money
from app.database.repo import MoneyRepo
from app.filters import StatusFilter
from app.handlers.models.expenses import ExpensesHandlers
from app.keyboards import get_menu_default
from app.keyboards import keyboard_builder
from app.logic.checks import check_input
from app.logic.expenses import borrowed_logic
from app.logic.expenses import expenses_logic
from app.logic.expenses import get_expenses_month_logic
from app.routers import expenses_router as router
from loader import bot
from loader import dp


@router.message(Command("start"), StatusFilter("admin"))
async def _start(message: Message):
    await message.answer(text="<b>Функции</b>", reply_markup=get_menu_default())


@dp.callback_query(StatusFilter("admin"), lambda query: query.data == "button_expenses")
async def _expenses_list(callback_query: CallbackQuery):
    result_list: List[Expenses] = await get_expenses_month_logic()

    text = ""
    for item in result_list:
        text += f'\n{"--" * 15}'
        for key, value in item.model_dump().items():
            text += f"\n|{key}: <b>{value}</b>"

    text += f"\n\n| Итого : <b>{sum([item.summ for item in result_list])}</b>"
    text += f'\n{"--" * 15}'

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=text,
        reply_markup=get_menu_default(),
    )


@dp.callback_query(
    StatusFilter("admin"), lambda query: query.data.startswith("button_borrowed_")
)
async def _borrowed_list(callback_query: CallbackQuery):
    result_text = callback_query.data[len("button_") :].split("_")[-1]
    try:
        borrowed_id: int = int(result_text)
    except:
        borrowed_id = None

    result_list: List[Expenses] = await borrowed_logic(borrowed_id)
    buttons = []
    text = ""

    for item in result_list:
        buttons.append(
            InlineKeyboardButton(
                text=str(item.id), callback_data=f"button_borrowed_{str(item.id)}"
            )
        )
        text += f'\n{"--" * 15}'
        for key, value in item.model_dump().items():
            text += f"\n| {key}: <b>{value}</b>"

    text += f"\n\n| Итого : <b>{sum([item.summ for item in result_list])}</b>"
    text += f'\n{"--" * 15}'

    if buttons:
        text += "\n\n| Возврат:"
    buttons_id_borrowed = keyboard_builder(buttons)
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=text,
        reply_markup=buttons_id_borrowed if buttons else get_menu_default(),
    )


@dp.callback_query(StatusFilter("admin"), lambda query: query.data == "button_summ")
async def button_summ_handler(message: Message):

    result: Money = await MoneyRepo.get()

    text = ""
    text += f'\n{"--" * 15}'
    text += f"\n{result.total_money}"
    text += f'\n{"--" * 15}'

    await message.answer(text, reply_markup=get_menu_default())


@router.message(StatusFilter("admin"))
async def _expenses(message: Message):
    expense: Expenses = await check_input(message)
    if not expense:
        return

    result: ExpensesHandlers = await expenses_logic(expense)

    text = ""
    text += f'\n{"--" * 15}'
    text += f"\n| Затрачено за текущий месяц: <b>{result.summ_period}</b>"
    text += f"\n| Должны: <b>{result.summ_borrowed}</b>"
    text += f"\n| остаток: <b>{result.summ}</b>"
    text += f'\n{"--" * 15}'

    await message.answer(text, reply_markup=get_menu_default())
