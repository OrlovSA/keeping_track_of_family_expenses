from typing import List

from app.database.models.user import User
from app.database.repo import UsersRepo


async def get_users_data_logic():
    users: List[User] = await UsersRepo.get_list()
    if not users:
        return "Users is empty🫡", None
    text = ""
    for user in users:
        text += f'\n{"--" * 15}'
        for key, value in user.model_dump().items():
            if key == "username" and value:
                text += f"\n|{key}: <tg-spoiler><b>@{value}</b></tg-spoiler>"
            else:
                text += f"\n|{key}: <b>{value}</b>"
    return text, None
