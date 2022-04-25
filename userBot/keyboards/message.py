import re
from datetime import date
import datetime

from userBot.handlers.utils import change_date_format

START_MESSAGE = 'Стартовое сообщение'
MAIN_MENU_MESSAGE = "Продолжим и найдем тот самый звук?"
PACKS_MESSAGE = ''
TEN_PACKS_MESSAGE = 'Показать ТОП-10'
WELCOME_PACKS_MESSAGE = 'Чтобы послушать пак ответьте на сообщение со списком цифрой номера нужного пака'

PACKS_GENRES_EMPTY = 'Паков пока нет'
DOWNLOAD_PACK = 'Понравился пак ?'
DOWNLOAD_PACK_MESSAGE = 'Чтобы скачать звук, ответь что угодно на сообщение с названием.\n\n' \
                        'Загружаем пак - '
BUY_PACK = 'Вы можете купить этот лимитированный пак и использовать в своих работах. Оформляем?'
EXCLUSIVE_CONTENT_EMPTY = 'Экслюзивные паки отсутствуют'
DELAY_MESSAGE_PACK = "Пак появится в боте-хранилище"

NEED_PAYMENT = "Чтобы скачать любой звук в высоком качестве (.wav) — оформите подписку на наш сервис." \
               "\n\nДля этого зайдите в раздел “Аккаунт” → “Подписка”"
PAYMENT_TITLE_MESSAGE = 'Подписка на'
PAYMENT_PACK = 'Покупка пака - '
PAYMENT_PACK_SUCCESS = 'Спасибо за покупку пака'
PAYMENT_PACK_MESSAGE = 'СООБЩЕНИЕ КОТОРОЕ НУЖНО ЗАПОЛНИТЬ 14 (ОПИСАНИЕ пка я хз можно хранить)'


def PAYMENT_BODY_MESSAGE(sub_to, days):
    if sub_to is None or sub_to < date.today():
        return f"Подписка будет действовать до {change_date_format(date.today() + datetime.timedelta(days=days)).replace('-', '.')}\n"
    elif sub_to > date.today():
        return f"Подписка будет действовать c {change_date_format(sub_to).replace('-', '.')} до " \
               f"{change_date_format(sub_to + datetime.timedelta(days=days)).replace('-', '.')}\n"

PAYMENT_SUCCESFULL = """Поздравляем! Платеж успешно прошел и мы рады видеть вас в нашем сообществе!

Подпишитесь на закрытый канал, чтобы получить доступ к контенту — ссылка """

PAYMENT_MESSAGE = """\n
В нее входит возможность скачивать все звуки в высоком качестве и доступ к закрытому контенту нашего сообщества (посмотреть расписание можно ТУТ)

При покупке 3 месяцев сразу — хх% скидка
При покупке на год — хх% на год

Выберите на какое количество месяцев вы хотите подписку?
    """


def DELAY_MESSAGE_SOUND(sound):
    return f"Звук {sound}  появится в боте-хранилище"


SOUNDS_LIMIT = 'Выгружено 50 звуков'

SOUNDS_MESSAGE = "Выберите следующий раздел"
DOWNLOAD_LIB_MESSAGE = 'Скоро пришлем - '

DRUMS_MESSAGE = 'Выберите категорию'
MELODIES_MESSAGE = 'Выберите категорию'

SOUND_MESSAGE = 'Чтобы скачать звук, выбери сообщение с его названием и ответь на ' \
                'него любой буквой\n\nЗагружаю звуки...'

SOUND_MESSAGE_EMPTY = '"Сейчас в этой категории нет паков/звуков'

NOT_SUB = 'Для скачивания звуков в высоком качестве — подпишитесь на бота-хранилище .\n' \
          'В него добавляются все скачанные файлы - это твоя библиотека паков/звуков'

ACCOUNT_MESSAGE = 'Здесь все про тебя'
REF_MESSAGE = 'Вы можете получить бесплатный месяц подписки за каждого оплатившего друга, который перейдет по вашей ' \
              'реферальной ссылке. Вы можете пригласить неограниченное количество друзей и ваши месяцы будет складываться'

GENRES_MESSAGE = 'Выберите категорию'

UPDATE_MESSAGE = 'База звуков обновилась'
