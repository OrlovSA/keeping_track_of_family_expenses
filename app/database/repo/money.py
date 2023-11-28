from pydantic import BaseModel
from pymongo.collection import Collection

from ..models import Money
from ..models import money_collection
from .base import BaseRepo


class MoneyRepo(BaseRepo):
    model: BaseModel = Money
    collection: Collection = money_collection

    @classmethod
    async def update_or_create(cls, data: Money) -> Money:
        result = await cls.collection.find_one_and_replace(
            {}, data.model_dump(), upsert=True, return_document=True
        )
        return Money(**result)
