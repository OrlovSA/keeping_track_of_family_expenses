from aiogram import Dispatcher

from app.filters import StatusFilter
import app.handlers.error

from .admins import router as admin_router
from .expenses import router as expenses_router


def setup_handlers(dp: Dispatcher) -> None:
    admin_router.message.filter(StatusFilter("admin"))
    expenses_router.message.filter(StatusFilter("admin"))
    dp.include_routers(expenses_router, admin_router)
