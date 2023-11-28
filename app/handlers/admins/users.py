from aiogram.filters import Command
from aiogram.types import Message

from app.filters import StatusFilter
from app.logic.users import get_users_data_logic
from app.routers import admin_router as router
from app.utils.logging import logger


@router.message(Command("users"), StatusFilter("super_admin"))
async def _users(message: Message):
    text, markup = await get_users_data_logic()
    logger.info(text)
    await message.answer(text, reply_markup=markup)
