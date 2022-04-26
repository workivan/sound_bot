from userBot import config
from userBot.keyboards.keyboard import SoundsKeyboard
from userBot.services.delay_service import send_file
from userBot.services.utils_service import Utils
from userBot.keyboards import message as msg


async def get_sound_by_type(message, fr=0, sound_type=None):
    type_id = Utils.remove_s_if_need(message.text.lower()) if not sound_type else sound_type
    sounds = await config.storage.get_sounds_by_type(type_id, config.QUERY_SOUNDS_LIMIT, fr)
    sounds_count = await config.storage.get_sounds_count_by_type(type_id)

    if len(sounds) != 0:

        for sound in sounds:
            try:
                await config.bot.send_message(
                    message.chat.id,
                    sound.name
                )
                await config.bot.send_voice(
                    message.chat.id,
                    voice=open(sound.path, 'rb')
                )
            except RuntimeError:
                await get_sound_by_type(message, fr)

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
            msg.SOUND_MESSAGE_EMPTY
        )


async def reply_for_sounds(message, reply_text, sound):
    await config.bot.send_message(
        message.chat.id,
        msg.DELAY_MESSAGE_SOUND(reply_text)
    )
    await send_file(message.chat.id, sound)
