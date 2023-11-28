from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from app.database.models.user import User
from app.database.repo import UsersRepo


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if event.message:
            from_user = event.message.from_user
        if event.callback_query:
            from_user = event.callback_query.from_user
        if event.inline_query:
            from_user = event.inline_query.from_user

        user: User = await UsersRepo.get_or_create(
            data=User(
                id=from_user.id,
                name=from_user.full_name,
                username=from_user.username,
            ),
        )
        data["user"] = user
        return await handler(event, data)
