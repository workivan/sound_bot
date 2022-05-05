import datetime

from aiogram import types

from userBot import config
from userBot.handlers.utils import change_date_format, is_user_connected
from userBot.keyboards.labels import ONE_MONTH_LABEL, THREE_MONTH_LABEL, ONE_YEAR_LABEL, PACK_PAYMENT
from userBot.keyboards import message as msg
from userBot.services.delay_service import send_file


class Payments:
    @staticmethod
    def get_subscribe_month():
        return [
            types.LabeledPrice(ONE_MONTH_LABEL, amount=14900),
        ]

    @staticmethod
    def get_price_fr_pack(pack):
        return [
            types.LabeledPrice(PACK_PAYMENT, amount=pack.cost),
        ]

    @staticmethod
    def get_subscribe_th_month():
        return [
            types.LabeledPrice(THREE_MONTH_LABEL, amount=39000),
        ]

    @staticmethod
    def get_subscribe_year():
        return [
            types.LabeledPrice(ONE_YEAR_LABEL, amount=139000),
        ]

    @staticmethod
    def current_sub_info(user):
        if user.subscription_to is not None and user.subscription_to > datetime.date.today():
            sub = change_date_format(str(user.subscription_to))
            return f"Текущая подписка действует до {sub.replace('-', '.')}." \
                   f" Мы напомним вам об оплате за несколько дней до истечения срока подписки.", True
        else:
            return 'У вас сейчас нет подписки на наш сервис', False

    @staticmethod
    async def check_is_sub(user, chat_id, message):
        if user.subscription_to is None or user.subscription_to < datetime.date.today():
            await config.bot.send_message(
                chat_id,
                message
            )
            return False
        return True

    @staticmethod
    async def pay_for_pack(pmnt, message, user):
        pack_name = pmnt.get("invoice_payload")
        pack = await config.storage.get_pack_by_name(pack_name)
        await config.storage.set_pay(message.chat.id, pack.path, pmnt.get("total_amount") / 100)

        connected = await is_user_connected(user, message.chat.id, msg.NOT_SUB_BUY_PACK)
        if not connected:
            return

        await send_file(message.chat.id, pack)
        await config.storage.update_pays(message.chat.id, pack.path)
        await config.bot.send_message(
            message.chat.id,
            msg.PAYMENT_PACK_SUCCESS
        )
        await config.bot.send_message(
            message.chat.id,
            msg.DELAY_MESSAGE_PACK
        )

    @staticmethod
    async def pay_for_sub(user, message, period):
        subscription = user.subscription_to if user.subscription_to and user.subscription_to > datetime.date.today()\
            else datetime.date.today()

        await config.storage.update_sub(
            message.chat.id,
            subscription + datetime.timedelta(days=period)
        )
        await config.bot.send_message(
            message.chat.id,
            msg.PAYMENT_SUCCESFULL
        )


