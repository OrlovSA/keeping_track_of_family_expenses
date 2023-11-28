from aiogram.types import BotCommand
from aiogram.types import BotCommandScopeDefault

from loader import bot


def get_default_commands():
    commands = [
        BotCommand(command="/summ", description=("Узнать остаток")),
        BotCommand(command="/expenses", description=("все затраты за текущий месяц")),
    ]

    return commands


async def set_default_commands():
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
