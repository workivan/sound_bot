import asyncio
import os

import psycopg2
import schedule
import datetime

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

DB_USER = 'ikuzin'
DB_NAME = 'sound_market'
DB_USER_PASSWORD = 'Pabotahard1$'
DB_URL = f"postgresql://{DB_USER}:{DB_USER_PASSWORD}@localhost:5432/{DB_NAME}"
API_TOKEN_MAIN_BOT = os.getenv("USER_BOT_TOKEN")
main_bot = Bot(token=API_TOKEN_MAIN_BOT)


async def send_message(chat_id):
    await main_bot.send_message(
        chat_id,
        "Через 3 дня Ваша подписка закончится. Успейте ее продлить!"
    )


def job():
    connection = psycopg2.connect("dbname='sound_market' user='ikuzin' host='localhost' password='Pabotahard1$'")
    cursor = connection.cursor()

    date_expires = datetime.date.today() + datetime.timedelta(days=3)

    cursor.execute(f"""select * from "user" where subscription_to='{date_expires}'""")
    for row in cursor:
        asyncio.run(send_message(row[0]))


schedule.every().day.at("12:00").do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
