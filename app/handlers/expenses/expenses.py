from typing import List

from aiogram.filters import Command
from aiogram.types import Message

from app.database.models.expenses import Expenses
from app.database.models.money import Money
from app.database.repo import MoneyRepo
from app.filters import StatusFilter
from app.handlers.models.expenses import ExpensesHandlers
from app.logic.checks import check_input
from app.logic.expenses import expenses_logic
from app.logic.expenses import get_expenses_month_logic
from app.routers import expenses_router as router


@router.message(Command("expenses"), StatusFilter("admin"))
async def _expenses(message: Message):
    result_list: List[Expenses] = await get_expenses_month_logic()

    text = ""
    for item in result_list:
        text += f'\n{"--" * 15}'
        for key, value in item.model_dump().items():
            text += f"\n|{key}: <b>{value}</b>"

    text += f"\n\n| Итого : <b>{sum([item.summ for item in result_list])}</b>"
    text += f'\n{"--" * 15}'

    await message.answer(text)


@router.message(Command("summ"), StatusFilter("admin"))
async def _summ(message: Message):
    result: Money = await MoneyRepo.get()

    text = ""
    text += f'\n{"--" * 15}'
    text += f"\n<b>{result.total_money}</b>"
    text += f'\n{"--" * 15}'

    await message.answer(text)


@router.message(StatusFilter("admin"))
async def _expenses_list(message: Message):
    expense: Expenses = await check_input(message)
    if not expense:
        return

    result: ExpensesHandlers = await expenses_logic(expense)

    text = ""
    text += f'\n{"--" * 15}'
    text += f"\n| Затрачено за текущий месяц: <b>{result.summ_period}</b>"
    text += f"\n| остаток: <b>{result.summ}</b>"
    text += f'\n{"--" * 15}'

    await message.answer(text)
