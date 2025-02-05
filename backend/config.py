from os import getenv
from dotenv import load_dotenv
from pathlib import Path
import pytz

BASE_DIR = Path(__file__).parent.resolve()

ENV_FILE = BASE_DIR.joinpath(getenv('ENV')) if getenv('ENV') else BASE_DIR.joinpath('.localenv')

load_dotenv(ENV_FILE)

DEBUG = bool(getenv('DEBUG', 1))

ENGINE = getenv('ENGINE', 'sqlite+aiosqlite:///./database/database.db')

REDIS_HOST = getenv('REDIS_HOST', "localhost")
REDIS_PORT = getenv('REDIS_HOST', 6379)

TIMEZONE = pytz.timezone(getenv('TIMEZONE', 'Europe/Moscow'))


BOT_TOKEN = getenv('BOT_TOKEN')
TEST_MODE = False
TEST_USER = dict(id=7485502073)

WEBHOOK_PATH = '/webhook'
WEBHOOK_HOST = getenv('WEBHOOK_HOST')
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

WEBAPP_URL = getenv('WEBAPP_URL')