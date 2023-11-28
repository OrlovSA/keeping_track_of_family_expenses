from aiogram.types import BotCommandScopeChat

from loader import bot

from .admins import set_admins_commands
from .default import set_default_commands


async def remove_admins_commands(id: int):
    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=id))
