from pydantic import BaseModel
from pydantic import Field
from pymongo.collection import Collection

from loader import db


class Money(BaseModel):
    total_money: float = Field(default=0.0)


money_collection: Collection = db["money"]
