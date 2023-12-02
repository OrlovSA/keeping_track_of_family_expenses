from datetime import datetime
from datetime import timedelta
from typing import List

from app.database.models import Expenses
from app.database.models import Money
from app.database.repo import ExpensesRepo
from app.database.repo import MoneyRepo
from app.handlers.models.expenses import ExpensesHandlers
from app.logic.enums import ExpensesStatusEnum


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

    if expense.status == ExpensesStatusEnum.delete:
        result: Expenses = await ExpensesRepo.get(id=int(expense.summ))
        await ExpensesRepo.collection.delete_one({"id": result.id})
        money.total_money += result.summ
    else:
        money.total_money = (
            money.total_money + expense.summ
            if expense.status == ExpensesStatusEnum.arrived
            else money.total_money - expense.summ
        )

    result_money: Money = await MoneyRepo.update_or_create(money)

    if not expense.status == ExpensesStatusEnum.delete:
        await ExpensesRepo.create(expense)

    result_list: List[Expenses] = await get_expenses_month_logic()

    summ_period = 0
    summ_borrowed = 0
    for item in result_list:
        summ_period += item.summ
        if item.status == ExpensesStatusEnum.borrowed:
            summ_borrowed += item.summ

    return ExpensesHandlers(
        summ_period=summ_period,
        summ=result_money.total_money,
        summ_borrowed=summ_borrowed,
    )


async def borrowed_logic(borrowed_id: int | None = None) -> List[Expenses]:
    if borrowed_id:
        result_expenses: Expenses = await ExpensesRepo.get(borrowed_id)
        money: Money = await MoneyRepo.get()
        money.total_money += result_expenses.summ
        await MoneyRepo.update_or_create(money)
        await ExpensesRepo.collection.delete_one({"id": borrowed_id})

    return await ExpensesRepo.search(status=ExpensesStatusEnum.borrowed)
