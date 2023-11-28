from datetime import datetime
from datetime import timedelta
from typing import List

from app.database.models import Expenses
from app.database.models import Money
from app.database.repo import ExpensesRepo
from app.database.repo import MoneyRepo
from app.handlers.models.expenses import ExpensesHandlers


async def get_expenses_month_logic() -> List[Expenses]:
    date_start = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    date_end = (date_start + timedelta(days=32)).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    return await ExpensesRepo.search(date_start=date_start, date_end=date_end)


async def expenses_logic(expense: Expenses) -> ExpensesHandlers:
    money: Money | None = await MoneyRepo.get()
    if not money:
        money = Money()

    money.total_money = (
        money.total_money + expense.summ
        if expense.is_replenishment
        else money.total_money - expense.summ
    )
    result_money: Money = await MoneyRepo.update_or_create(money)
    await ExpensesRepo.create(expense)

    result_list: List[Expenses] = await get_expenses_month_logic()

    return ExpensesHandlers(
        summ_period=sum([item.summ for item in result_list]),
        summ=result_money.total_money,
    )
