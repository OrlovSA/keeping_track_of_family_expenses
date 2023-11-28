from enum import Enum


class UserStatusEnum(str, Enum):
    user = "user"
    admin = "admin"
    super_admin = "super_admin"
