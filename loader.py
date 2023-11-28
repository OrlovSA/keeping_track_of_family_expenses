from aiogram import Bot, Dispatcher
from motor.motor_tornado import MotorClient

from app.data.config import (
    MONGO_URL,
    TELEGRAM_BOT_TOKEN,
)

bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")

from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

dp = Dispatcher(storage=storage)
client = MotorClient(MONGO_URL)
db = client['bot']
