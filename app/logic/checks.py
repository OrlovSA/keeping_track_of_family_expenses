from aiogram.types import Message

from app.database.models.expenses import Expenses
from app.database.repo import ExpensesRepo
from app.logic.enums import ExpensesStatusEnum
from app.utils.logging import logger


arrived_to_check = (
    ExpensesStatusEnum.arrived,
    "add",
    "зарплата",
    "аванс",
    "доход",
    "добавить",
    "внесение",
    "прибавление",
    "плюс",
    "прибавить" "+",
)
gone_to_check = (
    ExpensesStatusEnum.borrowed,
    "занял",
    "займ",
    "долг",
)
delete_to_check = (
    ExpensesStatusEnum.delete,
    "удалить",
    "вернуть",
    "отменить",
)


async def check_input(message: Message) -> Expenses:
    try:
        divider: int = message.text.index(" ")
    except Exception:
        error_text = f"Ошибка ввода: {message.text=}, нет пробела после суммы!\n\
            <b>Пример: 123 Пирашки с Котятами</b>\n<b>Пример: 123 add зарплата</b>"
        logger.error(error_text)
        await message.answer(error_text)
        return

    summ_in: str = message.text[:divider].strip().replace(",", ".")
    text: str = message.text[divider:].strip()

    try:
        summ = float(summ_in)
    except Exception:
        error_text = f"Ошибка ввода: {summ_in=}, херня сумма!\n\
            <b>Пример: 123</b>\n<b>Пример: 123.00</b>"
        logger.error(error_text)
        await message.answer(error_text)
        return
    text_lower = text.lower()

    if any(value in text_lower for value in arrived_to_check):
        status = ExpensesStatusEnum.arrived
    elif any(value in text_lower for value in gone_to_check):
        status = ExpensesStatusEnum.borrowed
    elif any(value in text_lower for value in delete_to_check):
        status = ExpensesStatusEnum.delete
        result: Expenses | None = await ExpensesRepo.get(id=int(summ))
        if not result:
            error_text = f"Ошибка ввода: {int(summ)}, нет такого id для удаления"
            logger.error(error_text)
            await message.answer(error_text)
            return
    else:
        status = ExpensesStatusEnum.gone

    return Expenses(
        id=message.message_id,
        text=text,
        summ=summ,
        username=message.from_user.first_name,
        status=status,
    )
