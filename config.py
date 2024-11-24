import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def boolean(value: str | bool | int):
    if isinstance(value, bool):
        return value
    value = str(value).lower()

    if value.isdigit():
        return False if value == "0" else True

    return {"false": False, "true": True}.get(value, bool(value))


def env(key, default=None):
    value = os.environ.get(key)
    if value:
        return value
    return default


BASE_DIR = Path(__file__).parent.resolve()

DEV_MODE = boolean(env('DEVMODE', False))

TEST_MODE = not DEV_MODE
TEST_USER_ID = 7485502073

PORT = 4550

HOST = env('HOST', 'https://2771-2a01-4f8-c012-3738-00-1.ngrok-free.app')
BOT_TOKEN = env('BOT_TOKEN', '7489777184:AAHk-tgEypNOTMa3gSW72c10FsgELmPH99o')
ENGINE = env('ENGINE', "sqlite+aiosqlite:///./database/database.db")

WEBAPP_URL = HOST
WEBHOOK_HOST = HOST
WEBHOOK_PATH = ''

ADMIN_USERNAME = ''
ADMIN_PASSWORD = ''
