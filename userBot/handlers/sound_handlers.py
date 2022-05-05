from userBot import config
from userBot.handlers.payment_handlers import Payments
from userBot.handlers.utils import is_user_connected
from userBot.keyboards.keyboard import SoundsKeyboard
from userBot.services.delay_service import send_file
from userBot.services.utils_service import Utils
from userBot.keyboards import message as msg


async def get_sound_by_type(message, fr=0, sound_type=None):
    type_id = Utils.remove_s_if_need(message.text.lower()) if not sound_type else sound_type
    sounds = await config.storage.get_sounds_by_type(type_id, config.QUERY_SOUNDS_LIMIT, fr)
    sounds_count = await config.storage.get_sounds_count_by_type(type_id)

    if len(sounds) != 0:
        for sound in sounds[:-1]:
            await config.bot.send_audio(
                message.chat.id,
                audio=open(sound.path, 'rb'),
                protect_content=True
            )

        if sounds_count > config.QUERY_SOUNDS_LIMIT + fr:
            await config.bot.send_audio(
                message.chat.id,
                audio=open(sounds[-1].path, 'rb'),
                reply_markup=SoundsKeyboard.get_more(fr + config.QUERY_SOUNDS_LIMIT, type_id)
            )
        else:
            await config.bot.send_audio(
                message.chat.id,
                audio=open(sounds[-1].path, 'rb')
            )
    else:
        await config.bot.send_message(
            message.chat.id,
            msg.SOUND_MESSAGE_EMPTY
        )


async def reply_for_sounds(message, audio):
    chat_id = message.chat.id
    sound = await config.storage.get_sound_by_name(audio.file_name)

    if sound:
        user = await config.storage.get_user(chat_id)
        sub = await Payments.check_is_sub(user, chat_id, msg.NEED_PAYMENT)
        if not sub:
            return

        connected = await is_user_connected(user, chat_id, msg.NOT_SUB)
        if not connected:
            return

    await config.bot.send_message(
        message.chat.id,
        msg.DELAY_MESSAGE_SOUND(audio.file_name)
    )
    await send_file(message.chat.id, sound)
