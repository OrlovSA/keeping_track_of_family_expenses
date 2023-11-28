from typing import List
from typing import TypeVar

from pydantic import BaseModel
from pymongo.collection import Collection
from pymongo.results import InsertOneResult


_Collection = TypeVar("_Collection", bound=Collection)
_Model = TypeVar("_Model", bound=BaseModel)


class BaseRepo:
    model: BaseModel = _Model
    collection: Collection = _Collection

    @classmethod
    async def get_list(cls) -> List[model]:
        result_list: List[dict] = cls.collection.find()
        return [cls.model(**value) async for value in result_list]

    @classmethod
    async def get(cls, id: int | None = None) -> model | None:
        requests = {"id": id} if id else {}
        result: dict = await cls.collection.find_one(requests)
        return cls.model(**result) if result else None

    @classmethod
    async def create(cls, data: model) -> model:
        result: InsertOneResult = await cls.collection.insert_one(
            data.model_dump(exclude_none=True)
        )
        return await cls.get(result.inserted_id)

    @classmethod
    async def update(cls, id: int, data: model) -> model:
        user: dict = await cls.collection.find_one_and_update(
            {"id": id},
            {"$set": data.model_dump(exclude_none=True)},
            return_document=True,
        )
        return cls.model(**user)
