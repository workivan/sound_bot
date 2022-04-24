import os

from aiogram import Bot
from dotenv import load_dotenv

from global_config import ROOT_DIR
from userBot.storage.storage import Storage

load_dotenv()

API_TOKEN_USER_BOT = os.getenv("USER_BOT_TOKEN")
API_PAY_TOKEN='381764678:TEST:36367'

SHOP_ID = 506751
SHOP_ARTICLE_ID = 538350

# webhook settings
WEBHOOK_HOST = 'https://62.113.107.163'
WEBHOOK_PATH = '/userBot/handler.py'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001

DB_USER = 'ikuzin'
DB_NAME = 'sound_market'
DB_USER_PASSWORD = 'Pabotahard1$'
DB_URL = f"postgresql://{DB_USER}:{DB_USER_PASSWORD}@localhost:5432/{DB_NAME}"

bot = Bot(token=API_TOKEN_USER_BOT)

storage = Storage()

QUERY_LIMIT = 3
QUERY_RATE_LIMIT = 10
QUERY_SOUNDS_LIMIT = 3

TMP_FILES_DIR = ROOT_DIR + "/upload/"

TELEGRAM_REF = 'https://telegram.me/?start='
