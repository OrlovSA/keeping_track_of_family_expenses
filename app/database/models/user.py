from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pymongo.collection import Collection

from app.logic.enums import UserStatusEnum
from loader import db


class User(BaseModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    status: Optional[UserStatusEnum] = Field(default=None)


users_collection: Collection = db["users"]
