from aiogram import types

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
        return f"Текущая подписка действует до {user.subscription_to}"
