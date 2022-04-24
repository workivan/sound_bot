from datetime import date

from aiogram import types

from userBot.handlers.utils import change_date_format
from userBot.keyboards.labels import ONE_MONTH_LABEL, THREE_MONTH_LABEL, ONE_YEAR_LABEL, PACK_PAYMENT


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
        if user.subscription_to is not None and user.subscription_to > date.today():
            sub = change_date_format(str(user.subscription_to))
            return f"Текущая подписка действует до {sub.replace('-','.')}." \
                   f" Мы напомним вам об оплате за несколько дней до истечения срока подписки."
        else:
            return 'У вас сейчас нет подписки на наш сервис'
