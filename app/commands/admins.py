from aiogram.types import BotCommand
from aiogram.types import BotCommandScopeChat

from loader import bot

from .default import get_default_commands


def get_admins_commands():
    commands = get_default_commands()
    commands.extend(
        [BotCommand(command="/users", description=("get users list [admin]"))]
    )
    return commands


async def set_admins_commands(id: int):
    await bot.set_my_commands(
        get_admins_commands(), scope=BotCommandScopeChat(chat_id=id)
    )
