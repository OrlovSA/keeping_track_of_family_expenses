from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pymongo.collection import Collection

from app.logic.enums import ExpensesStatusEnum
from loader import db


class Expenses(BaseModel):
    id: Optional[int] = Field(default=None)
    status: Optional[ExpensesStatusEnum] = Field(default=None)
    text: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    summ: Optional[float] = Field(default=None)
    create_date: datetime = Field(default_factory=datetime.now)


expenses_collection: Collection = db["expenses"]
