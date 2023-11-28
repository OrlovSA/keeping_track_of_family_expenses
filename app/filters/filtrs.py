from aiogram.filters import Filter
from aiogram.types import Message

from app.commands import remove_admins_commands
from app.database.models.user import User
from app.logic.enums import UserStatusEnum
from app.utils.logging import logger


class StatusFilter(Filter):
    def __init__(self, status: str) -> None:
        if status == UserStatusEnum.admin:
            self.statuses = [UserStatusEnum.admin, UserStatusEnum.super_admin]
        else:
            self.statuses = UserStatusEnum.super_admin

    async def __call__(self, message: Message, **data: dict) -> bool:
        user: User = data["user"]
        logger.info(f"{message.text=} | {user=}")

        _is = user.status in self.statuses
        if not _is:
            await remove_admins_commands(user.id)
            await message.answer(("Not enough rights🚫"))
        return _is
