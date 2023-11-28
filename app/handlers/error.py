from aiogram.types import ErrorEvent

from app.utils import logger
from loader import dp


@dp.error()
async def _error(event: ErrorEvent):
    logger.warning(event.exception)
