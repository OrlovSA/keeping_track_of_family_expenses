from aiogram.types import Message

from app.database.models.expenses import Expenses
from app.utils.logging import logger


async def check_input(message: Message) -> Expenses:
    try:
        divider: int = message.text.index(" ")
    except Exception:
        error_text = f"Ошибка ввода: {message.text=}, нет пробела после суммы!\n\
            <b>Пример: 123 Пирашки с Котятами</b>\n<b>Пример: 123 add зарплата</b>"
        logger.error(error_text)
        await message.answer(error_text)
        return

    summ_in: str = message.text[:divider]
    text: str = message.text[divider:].strip()

    try:
        summ = float(summ_in)
    except Exception:
        error_text = f"Ошибка ввода: {summ_in=}, херня сумма!\n\
            <b>Пример: 123</b>\n<b>Пример: 123.00</b>"
        logger.error(error_text)
        await message.answer(error_text)
        return

    return Expenses(
        text=text,
        summ=summ,
        username=message.chat.first_name,
        is_replenishment=True if "add" in text.lower() else False,
    )
