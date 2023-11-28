from app.database.models.user import User
from app.database.models.user import users_collection
from app.logic.enums import UserStatusEnum

from .base import BaseRepo


class UsersRepo(BaseRepo):
    model = User
    collection = users_collection

    @classmethod
    async def get_or_create(cls, data: model) -> model:
        result_item: cls.model | None = await cls.get(data.id)
        if result_item:
            return await cls.update(data.id, data)

        data.status = UserStatusEnum.user
        return await cls.create(data)
