from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from userBot import config
from userBot.keyboards import message as msg
from userBot.services.referral_service import ReferralService


class AuthMiddleware(BaseMiddleware):
    def __init__(self, key_prefix='no_subcribe_'):
        self.prefix = key_prefix
        super(AuthMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user = await ReferralService.get_or_create_user(message.from_user, message.text)

        if not user.is_connected:
            await config.bot.send_message(
                message.chat.id,
                msg.NOT_SUB + '\n' + '',
            )
            await config.bot.send_message(
                message.chat.id,
                'https://telegram.me/sound_market_echo_dev_bot'
            )
            raise CancelHandler()
