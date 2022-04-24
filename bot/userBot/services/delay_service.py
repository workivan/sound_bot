import os
import shutil
from pathlib import Path
from zipfile import ZipFile
from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from bot.userBot import config
from bot.userBot.services.upload_service import Uploader
from bot.userBot.keyboards import message as msg

load_dotenv()

API_TOKEN_USER_BOT = os.getenv("ECHO_BOT_TOKEN")
echo_bot = Bot(token=API_TOKEN_USER_BOT)
echo_dp = Dispatcher(echo_bot)


@echo_dp.async_task
async def send_file(chat_id, file):
    temp_dir = config.TMP_FILES_DIR + Uploader.get_random_dir_name()
    os.mkdir(temp_dir)
    await echo_bot.send_message(
        chat_id,
        msg.DOWNLOAD_LIB_MESSAGE + file.name
    )
    if hasattr(file, 'genre'):
        with ZipFile(temp_dir + '/' + file.name + '.zip', 'w') as zf:
            for wav in Path(file.path).rglob('*'):
                if wav.name.startswith('.'):
                    continue
                zf.write(wav, wav.name)
        await echo_bot.send_document(
            chat_id,
            document=open(temp_dir + '/' + file.name + '.zip', 'rb')
        )
    else:
        await echo_bot.send_document(
            chat_id,
            document=open(file.path, 'rb')
        )
    shutil.rmtree(temp_dir + '/', ignore_errors=True)
