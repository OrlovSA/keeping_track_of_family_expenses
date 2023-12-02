from datetime import datetime
from typing import List

from pydantic import BaseModel
from pymongo import DESCENDING
from pymongo.collection import Collection

from app.logic.enums import ExpensesStatusEnum

from ..models import Expenses
from ..models import expenses_collection
from .base import BaseRepo


class ExpensesRepo(BaseRepo):
    model: BaseModel = Expenses
    collection: Collection = expenses_collection

    @classmethod
    async def create_index(cls) -> None:
        await cls.collection.create_index(
            [("create_date", DESCENDING), ("summ"), ("text"), ("status")]
        )
        await cls.collection.create_index("id", unique=True)

    @classmethod
    async def search(
        cls,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        search_text: str | None = None,
        status: ExpensesStatusEnum | None = None,
    ) -> List[Expenses]:
        query = dict()

        if not status:
            query = {
                "status": {
                    "$in": (ExpensesStatusEnum.gone, ExpensesStatusEnum.borrowed)
                }
            }
        else:
            query["status"] = status
        if date_start:
            query["create_date"] = {"$gte": date_start, "$lt": date_end or date_start}
        if search_text:
            query["text"] = {"$regex": f".*{search_text}.*", "$options": "i"}

        result_list: List[dict] = cls.collection.find(query)

        return [Expenses(**result) async for result in result_list]
