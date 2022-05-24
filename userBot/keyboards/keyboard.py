from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from userBot.keyboards.button import MenuButtons, PacksMenuButtons, SoundsMenuButtons, CommonButtons, DrumsButtons, \
    MelodiesButtons, AccountButtons, GenresButtons, MoreSoundsButtons, PaymentKeyboard
from userBot.keyboards.callback import PacksCallback, SoundCallback, PaymentCallback


class MenuKeyboard:
    @staticmethod
    def get_rk():
        rk = ReplyKeyboardMarkup(resize_keyboard=True)
        rk.row(
            KeyboardButton(MenuButtons.PACKS),
            KeyboardButton(MenuButtons.EXCLUSIVES)
        )
        rk.row(
            KeyboardButton(MenuButtons.SOUNDS),
            KeyboardButton(MenuButtons.GENRES)
        )
        rk.row(
            KeyboardButton(MenuButtons.ACCOUNT)
        )
        return rk


class AccountMenu:
    @staticmethod
    def get_rk():
        rk = ReplyKeyboardMarkup(resize_keyboard=True)
        rk.row(
            KeyboardButton(AccountButtons.ACC),
            KeyboardButton(AccountButtons.REF)
        )
        rk.add(KeyboardButton(CommonButtons.BACK_TO_MENU))
        return rk

    @staticmethod
    def get_pay():
        ik = InlineKeyboardMarkup(resize_keyboard=True)
        ik.row(InlineKeyboardButton(PaymentKeyboard.MONTH, callback_data=PaymentCallback.MONTH),
               InlineKeyboardButton(PaymentKeyboard.TH_MONTH, callback_data=PaymentCallback.TH_MONTH),
               InlineKeyboardButton(PaymentKeyboard.YEAR, callback_data=PaymentCallback.YEAR))

        return ik


class PacksKeyboard:
    @staticmethod
    def get_next_genres_pack(next_packs=None, genre=None):
        ik = InlineKeyboardMarkup(resize_keyboard=True)
        if next_packs:
            but = PacksMenuButtons.MORE if next_packs != -1 else PacksMenuButtons.FIRST
            ik.add(
                InlineKeyboardButton(
                    but,
                    callback_data=PacksCallback.MORE_PACKS(next_packs if next_packs >= 0 else 0, genre)))

        return ik

    @staticmethod
    def get_ten(next_packs=None):
        ik = InlineKeyboardMarkup(resize_keyboard=True)
        ik.add(InlineKeyboardButton(PacksMenuButtons.TEN, callback_data=PacksCallback.TEN))
        if next_packs:
            but = PacksMenuButtons.MORE if next_packs != -1 else PacksMenuButtons.FIRST
            ik.add(
                InlineKeyboardButton(but, callback_data=PacksCallback.MORE_PACKS(next_packs if next_packs >= 0 else 0)))
        return ik

    @staticmethod
    def get_filtred():
        ik = InlineKeyboardMarkup(resize_keyboard=True)
        ik.add(InlineKeyboardButton(PacksMenuButtons.FILTRED, callback_data=PacksCallback.FILTRED))
        return ik

    @staticmethod
    def get_buy(pack_name, bought):
        ik = InlineKeyboardMarkup(resize_keyboard=True)
        if bought:
            ik.add(
                InlineKeyboardButton(PacksMenuButtons.DOWNLOAD,
                                     callback_data=PacksCallback.DOWNLOAD_PACK(pack_name, bought)))
        else:
            ik.add(InlineKeyboardButton(PacksMenuButtons.BUY, callback_data=PacksCallback.BUY_PACK(pack_name)))
        ik.add(InlineKeyboardButton(PacksMenuButtons.PACKS, callback_data=PacksCallback.PACKS + ',vip'))
        return ik

    @staticmethod
    def get_download_g(pack_name, genres, genre=''):
        ik = InlineKeyboardMarkup(resize_keyboard=True)
        ik.add(InlineKeyboardButton(PacksMenuButtons.DOWNLOAD, callback_data=PacksCallback.DOWNLOAD_PACK(pack_name)))
        ik.add(InlineKeyboardButton(PacksMenuButtons.PACKS,
                                    callback_data=PacksCallback.PACKS + f',{genres.strip() if genres else " "}, {genre.strip()}'))
        return ik


class SoundsKeyboard:
    @staticmethod
    def get_rk_sounds():
        rk = ReplyKeyboardMarkup(resize_keyboard=True)
        rk.row(
            KeyboardButton(SoundsMenuButtons.DRUMS),
            KeyboardButton(SoundsMenuButtons.MELODIES)
        )
        rk.add(KeyboardButton(CommonButtons.BACK_TO_MENU))
        return rk

    @staticmethod
    def get_rk_drums():
        rk = ReplyKeyboardMarkup(resize_keyboard=True)
        rk.row(
            KeyboardButton(DrumsButtons.KICKS + 's'),
            KeyboardButton(DrumsButtons.SNARES + 's'),
            KeyboardButton(DrumsButtons.HATS + 's'),
            KeyboardButton(DrumsButtons.CLAPS + 's'),
            KeyboardButton(DrumsButtons.CYMBALS + 's'),
        )
        rk.row(
            KeyboardButton(DrumsButtons.PERCUSSIONS + 's'),
            KeyboardButton(DrumsButtons.FX),
            KeyboardButton(DrumsButtons.BASS),
            KeyboardButton(DrumsButtons.LOOPS + 's'),
            KeyboardButton(DrumsButtons.MORE),
        )
        rk.add(KeyboardButton(CommonButtons.BACK_TO_SOUNDS))
        return rk

    @staticmethod
    def get_rk_melodies():
        rk = ReplyKeyboardMarkup(resize_keyboard=True)
        rk.row(
            KeyboardButton(MelodiesButtons.GUITARS + 's'),
            KeyboardButton(MelodiesButtons.KEYS + 's'),
            KeyboardButton(MelodiesButtons.SYNTH),
            KeyboardButton(MelodiesButtons.VOCALS + 's'),
        )
        rk.row(
            KeyboardButton(MelodiesButtons.SAMPLES + 's'),
            KeyboardButton(MelodiesButtons.STRINGS + 's'),
            KeyboardButton(MelodiesButtons.MORE),
        )
        rk.add(KeyboardButton(CommonButtons.BACK_TO_SOUNDS))
        return rk

    @staticmethod
    def get_more(fr, sound_type):
        ik = InlineKeyboardMarkup(resize_keyboard=True)
        ik.add(InlineKeyboardButton(MoreSoundsButtons.MORE, callback_data=SoundCallback.FIFTY + f',{fr},{sound_type}'))
        return ik


class GenresKeyboard:
    @staticmethod
    def get_rk():
        rk = ReplyKeyboardMarkup(resize_keyboard=True)
        rk.row(
            KeyboardButton(GenresButtons.HIP_HOP),
            KeyboardButton(GenresButtons.RNB),
            KeyboardButton(GenresButtons.ROCK)
        )
        rk.row(
            KeyboardButton(GenresButtons.HOUSE_TECHNO),
            KeyboardButton(GenresButtons.POP),
            KeyboardButton(GenresButtons.DANCEHALL_AFRO),
            KeyboardButton(GenresButtons.MORE)
        )
        rk.add(KeyboardButton(CommonButtons.BACK_TO_MENU))
        return rk
