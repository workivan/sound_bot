import shutil

from bot.userBot import config
from bot.userBot.keyboards.keyboard import SoundsKeyboard
from bot.userBot.services.delay_service import send_file
from bot.userBot.services.upload_service import Uploader
from bot.userBot.services.utils_service import Utils
from bot.userBot.keyboards import message as msg


async def get_sound_by_type(message, fr=0, sound_type=None):
    type_id = Utils.remove_s_if_need(message.text.lower()) if not sound_type else sound_type
    sounds = await config.storage.get_sounds_by_type(type_id, config.QUERY_SOUNDS_LIMIT, fr)
    sounds_count = await config.storage.get_sounds_count_by_type(type_id)

    if len(sounds) != 0:
        ogg_files, tmp_dir = Uploader.upload_sounds_by_path(sounds)

        for ogg in ogg_files:
            try:
                with open(ogg.ogg_path, 'rb') as doc:
                    await config.bot.send_message(
                        message.chat.id,
                        ogg.name
                    )
                    await config.bot.send_voice(
                        message.chat.id,
                        voice=doc
                    )
            except RuntimeError:
                await get_sound_by_type(message, fr)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        if sounds_count > config.QUERY_SOUNDS_LIMIT + fr:
            await config.bot.send_message(
                message.chat.id,
                msg.SOUNDS_LIMIT,
                reply_markup=SoundsKeyboard.get_more(fr + config.QUERY_SOUNDS_LIMIT, type_id)
            )
            return
        else:
            await config.bot.send_message(
                message.chat.id,
                msg.FINISH_SOUNDS
            )
    else:
        await config.bot.send_message(
            message.chat.id,
            msg.SOUND_MESSAGE_EMPTY
        )


async def reply_for_sounds(message, reply_text):
    await config.bot.send_message(
        message.chat.id,
        msg.DELAY_MESSAGE_SOUND(reply_text)
    )
    sound = await config.storage.get_sound_by_name(reply_text)
    await send_file(message.chat.id, sound)
