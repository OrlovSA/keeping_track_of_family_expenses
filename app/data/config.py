from pathlib import Path

from environs import Env


env = Env()
env.read_env()

DIR = Path(__file__).absolute().parent.parent

TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")

MONGO_URL = env.str("MONGO_URL", None)

RATE_LIMIT = env.float("RATE_LIMIT", 0.5)
