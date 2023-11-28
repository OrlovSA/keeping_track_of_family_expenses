from datetime import datetime
from typing import Any
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator
from pymongo.collection import Collection

from loader import db


class Expenses(BaseModel):
    id: Optional[Any] = Field(default=None)
    is_replenishment: Optional[bool] = Field(default=None)
    text: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    summ: Optional[float] = Field(default=None)
    create_date: datetime = Field(default_factory=datetime.now)

    @root_validator(pre=True)
    def _add_id(cls, value: dict) -> dict:
        if value.get("_id"):
            value["id"] = value["_id"]

        return value


expenses_collection: Collection = db["expenses"]
