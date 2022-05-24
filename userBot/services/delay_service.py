import os
from pathlib import Path
from zipfile import ZipFile
from aiogram import Bot

from dotenv import load_dotenv

from userBot import config
from userBot.services.upload_service import Uploader
from userBot.keyboards import message as msg

load_dotenv()

API_TOKEN_USER_BOT = os.getenv("ECHO_BOT_TOKEN")
echo_bot = Bot(token=API_TOKEN_USER_BOT)


async def send_file(chat_id, file):
    await echo_bot.send_message(
        chat_id,
        msg.DOWNLOAD_LIB_MESSAGE + file.name
    )
    if hasattr(file, 'genre'):
        temp_dir = config.TMP_FILES_DIR + Uploader.get_random_dir_name()
        os.mkdir(temp_dir)
        zf = ZipFile(temp_dir + '/' + file.name + '.zip', 'w')
        for wav in Path(file.path).rglob('*'):
            if wav.name.startswith('.'):
                continue
            zf.write(wav, wav.name)
            if os.path.getsize(temp_dir + '/' + file.name + '.zip') > 50000000:

                zf.close()
                os.remove(temp_dir + '/' + file.name + '.zip')
                zf = ZipFile(temp_dir + '/' + file.name + '.zip', 'w')

                for wav1 in Path(file.path).rglob('*'):
                    if wav1.name.startswith('.'):
                        continue
                    if wav1.name == wav.name:
                        break
                    zf.write(wav1, wav1.name)
                await echo_bot.send_document(
                    chat_id,
                    document=open(temp_dir + '/' + file.name + '.zip', 'rb')
                )

                zf.close()
                os.remove(temp_dir + '/' + file.name + '.zip')
                zf = ZipFile(temp_dir + '/' + file.name + '.zip', 'w')
                zf.write(wav, wav.name)

        zf.close()
        await echo_bot.send_document(
            chat_id,
            document=open(temp_dir + '/' + file.name + '.zip', 'rb')
        )
        os.remove(temp_dir + '/' + file.name + '.zip')
        os.rmdir(temp_dir)

    else:
        await echo_bot.send_document(
            chat_id,
            document=open(file.path, 'rb')
        )
