import re
from datetime import date
from distutils.util import strtobool

from aiogram import types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType

from userBot import config
from userBot.handlers.pack_handlers import pack_by_genre_handler, pack_by_menu, reply_for_packs, exclusive_packs
from userBot.handlers.payment_handlers import Payments
from userBot.handlers.sound_handlers import get_sound_by_type, reply_for_sounds
from userBot.handlers.utils import send_message_to_u, lambda_for_packs_genres, lambda_for_sounds, to_sounds_filter, \
    lambda_sound
from userBot.keyboards import message as msg, button as bt, keyboard as kb
from userBot.keyboards.callback import PacksCallback, SoundCallback, PaymentCallback
from userBot.middleware import AuthMiddleware
from userBot.services.delay_service import send_file

dp = Dispatcher(config.bot, storage=MemoryStorage())
dp.middleware.setup(AuthMiddleware())


# меню
@dp.message_handler(lambda message: message.text and message.text.startswith("/start"))
async def start_message(message: types.Message):
    await send_message_to_u(message.chat.id, msg.START_MESSAGE, kb.MenuKeyboard.get_rk())


@dp.message_handler(lambda message: message.text and message.text == bt.CommonButtons.BACK_TO_MENU)
async def sounds_menu(message: types.Message):
    await send_message_to_u(message.chat.id, msg.MAIN_MENU_MESSAGE, kb.MenuKeyboard.get_rk())


# account
@dp.message_handler(lambda message: message.text and message.text == bt.MenuButtons.ACCOUNT)
async def get_account_menu(message: types.Message):
    await send_message_to_u(message.chat.id, msg.DRUMS_MESSAGE, kb.AccountMenu.get_rk())


@dp.message_handler(lambda message: message.text and message.text == bt.AccountButtons.REF)
async def get_ref(message: types.Message):
    user = await config.storage.get_user(message.chat.id)
    await send_message_to_u(message.chat.id, msg.REF_MESSAGE, None)
    await send_message_to_u(message.chat.id, config.TELEGRAM_REF + user.username, None)


# genres
@dp.message_handler(lambda message: message.text and message.text == bt.MenuButtons.GENRES)
async def get_genres(message: types.Message):
    await send_message_to_u(message.chat.id, msg.GENRES_MESSAGE, kb.GenresKeyboard.get_rk())


@dp.message_handler(lambda message: lambda_for_packs_genres(message))
async def get_packs_by_genre(message: types.Message, state):
    await send_message_to_u(message.chat.id, msg.WELCOME_PACKS_MESSAGE, None)
    await pack_by_genre_handler(message, state)


# Звуки
@dp.message_handler(lambda message: lambda_for_sounds(message))
async def sounds_menu(message: types.Message):
    await send_message_to_u(message.chat.id, msg.SOUNDS_MESSAGE, kb.SoundsKeyboard.get_rk_sounds())


@dp.message_handler(lambda message: message.text and message.text == bt.SoundsMenuButtons.MELODIES)
async def drums_menu(message: types.Message):
    await to_sounds_filter(message, msg.MELODIES_MESSAGE, kb.SoundsKeyboard.get_rk_melodies)


@dp.message_handler(lambda message: message.text and message.text == bt.SoundsMenuButtons.DRUMS)
async def melodies_menu(message: types.Message):
    await to_sounds_filter(message, msg.DRUMS_MESSAGE, kb.SoundsKeyboard.get_rk_drums)


@dp.message_handler(lambda message: lambda_sound(message))
async def get_sounds(message: types.Message):
    await send_message_to_u(message.chat.id, msg.SOUND_MESSAGE, None)
    await get_sound_by_type(message)


# payments

@dp.message_handler(lambda message: message.text and message.text == bt.AccountButtons.ACC)
async def get_subscribes(message):
    user = await config.storage.get_user(message.chat.id)
    await config.bot.send_message(
        message.chat.id,
        f'\n{Payments.current_sub_info(user)}' + msg.PAYMENT_MESSAGE,
        reply_markup=kb.AccountMenu.get_pay()
    )


# exclusive content
@dp.message_handler(lambda message: message.text and message.text == bt.MenuButtons.EXCLUSIVES)
async def get_exclusive_packs(message, state):
    await exclusive_packs(message, state)


# Паки

@dp.message_handler(lambda message: message.text and message.text == bt.MenuButtons.PACKS)
async def packs_menu(message: types.Message, state):
    async with state.proxy() as proxy:
        proxy['GENRES'] = False
        proxy['VIP'] = False
    await pack_by_menu(message)


@dp.async_task
@dp.message_handler()
async def replies_handler(message: types.Message, state):
    if message.reply_to_message is None:
        return

    replied_message_text = message.reply_to_message.text

    # ответ на звуки
    if replied_message_text.endswith('.wav'):
        chat_id = message.chat.id

        user = await config.storage.get_user(chat_id)

        if not user.is_connected:
            await config.bot.send_message(
                message.chat.id,
                msg.NOT_SUB + '\n' + '',
            )
            await config.bot.send_message(
                message.chat.id,
                'https://telegram.me/sound_market_echo_dev_bot'
            )
            return

        user = await config.storage.get_user(chat_id)
        if user.subscription_to is not None and user.subscription_to > date.today():
            await reply_for_sounds(message, replied_message_text)
            return
        await config.bot.send_message(
            chat_id,
            msg.NEED_PAYMENT
        )
    # ответ на паки
    if re.match('(\d+\))', replied_message_text):
        await reply_for_packs(message, replied_message_text, state)


# callbacks handlers
@dp.callback_query_handler(lambda cq: cq.data and cq.data.startswith(PacksCallback.DOWNLOAD))
async def callback_handler_download(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id

    user = await config.storage.get_user(chat_id)

    if not user.is_connected:
        await config.bot.send_message(
            callback_query.message.chat.id,
            msg.NOT_SUB + '\n' + '',
        )
        await config.bot.send_message(
            callback_query.message.chat.id,
            'https://telegram.me/sound_market_echo_dev_bot'
        )
        return

    args = callback_query.data.split(',')
    bought = False
    if len(args) == 3:
        bought = bool(strtobool(args[2]))
    user = await config.storage.get_user(chat_id)

    if bought:
        pack_name = args[1].strip()
        pack = await config.storage.get_pack_by_name(pack_name)
        await send_file(chat_id, pack)
        await config.bot.send_message(
            chat_id,
            msg.DELAY_MESSAGE_PACK
        )
        return
    if user.subscription_to and user.subscription_to > date.today():
        pack_name = args[1].strip()
        pack = await config.storage.get_pack_by_name(pack_name)
        await send_file(chat_id, pack)
        await config.bot.send_message(
            chat_id,
            msg.DELAY_MESSAGE_PACK
        )
        return

    await config.bot.send_message(
        chat_id,
        msg.NEED_PAYMENT
    )
    return


@dp.callback_query_handler(lambda cq: cq.data and cq.data.startswith(PacksCallback.BUY))
async def callback_handler_download(callback_query: types.CallbackQuery):
    pack_name = callback_query.data.split(',')[1].strip()
    pack = await config.storage.get_pack_by_name(pack_name)
    await config.bot.send_invoice(
        callback_query.message.chat.id,
        title=msg.PAYMENT_PACK + f' {pack_name}',
        description=msg.PAYMENT_PACK_MESSAGE,
        provider_token=config.API_PAY_TOKEN,
        currency='rub',
        is_flexible=False,
        prices=Payments.get_price_fr_pack(pack),
        start_parameter='time-machine-example',
        payload=pack_name
    )


@dp.callback_query_handler(lambda cq: cq.data and cq.data == PaymentCallback.MONTH)
async def get_price1(callback_query: types.CallbackQuery):
    user = await config.storage.get_user(callback_query.from_user.id)
    await config.bot.send_invoice(
        callback_query.message.chat.id,
        title=msg.PAYMENT_TITLE_MESSAGE + ' ' + callback_query.data,
        description=msg.PAYMENT_BODY_MESSAGE(user.subscription_to, 30),
        provider_token=config.API_PAY_TOKEN,
        currency='rub',
        is_flexible=False,
        prices=Payments.get_subscribe_month(),
        start_parameter='time-machine-example',
        payload=callback_query.data
    )


@dp.callback_query_handler(lambda cq: cq.data and cq.data == PaymentCallback.TH_MONTH)
async def get_price3(callback_query: types.CallbackQuery):
    user = await config.storage.get_user(callback_query.from_user.id)
    await config.bot.send_invoice(
        callback_query.message.chat.id,
        title=msg.PAYMENT_TITLE_MESSAGE + ' ' + callback_query.data,
        description=msg.PAYMENT_BODY_MESSAGE(user.subscription_to, 90),
        provider_token=config.API_PAY_TOKEN,
        currency='rub',
        is_flexible=False,
        prices=Payments.get_subscribe_th_month(),
        start_parameter='time-machine-example',
        payload=callback_query.data
    )


@dp.callback_query_handler(lambda cq: cq.data and cq.data == PaymentCallback.YEAR)
async def get_price2(callback_query: types.CallbackQuery):
    user = await config.storage.get_user(callback_query.from_user.id)
    await config.bot.send_invoice(
        callback_query.message.chat.id,
        title=msg.PAYMENT_TITLE_MESSAGE + ' ' + callback_query.data,
        description=msg.PAYMENT_BODY_MESSAGE(user.subscription_to, 360),
        provider_token=config.API_PAY_TOKEN,
        currency='rub',
        is_flexible=False,
        prices=Payments.get_subscribe_year(),
        start_parameter='time-machine-example',
        payload=callback_query.data
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await config.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    pmnt = message.successful_payment.to_python()
    if pmnt.get("invoice_payload") == PaymentCallback.YEAR:
        period = 360
    elif pmnt.get("invoice_payload") == PaymentCallback.TH_MONTH:
        period = 90
    elif pmnt.get("invoice_payload") == PaymentCallback.MONTH:
        period = 30
    else:
        pack_name = pmnt.get("invoice_payload")
        pack = await config.storage.get_pack_by_name(pack_name)
        await config.storage.set_pay(message.chat.id, pack_name, pmnt.get("total_amount") / 100)
        await send_file(message.chat.id, pack)
        await config.bot.send_message(
            message.chat.id,
            msg.PAYMENT_PACK_SUCCESS + f' {pmnt.get("invoice_payload")}'
        )
        await config.bot.send_message(
            message.chat.id,
            msg.DELAY_MESSAGE_PACK
        )
        return
    user = await config.storage.get_user(message.chat.id)
    await config.storage.update_sub(message.chat.id, period,
                                    user.subscription_to if user.subscription_to else 'CURRENT_DATE')
    await config.bot.send_message(
        message.chat.id,
        msg.PAYMENT_SUCCESFULL + f' {pmnt.get("invoice_payload")}'
    )


# TODO genres by 25, + get_list again
@dp.callback_query_handler(lambda cq: cq.data and cq.data == PacksCallback.GENRES)
async def callback_handler_genres(callback_query: types.CallbackQuery):
    return


@dp.callback_query_handler(lambda cq: cq.data and cq.data.startswith(SoundCallback.FIFTY))
async def callback_handler_more_sounds(callback_query: types.CallbackQuery):
    cq_args = callback_query.data.split(',')
    await config.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await get_sound_by_type(callback_query.message, int(cq_args[1]), cq_args[2])


@dp.callback_query_handler(lambda cq: cq.data and cq.data.startswith(PacksCallback.PACKS))
async def callback_handler_packs_again(callback_query: types.CallbackQuery, state):
    args = callback_query.data.split(',')

    if args[1] == 'vip':
        await exclusive_packs(callback_query.message, state)
    elif args[1] == 'genres':
        await send_message_to_u(callback_query.message.chat.id, msg.WELCOME_PACKS_MESSAGE, None)
        await pack_by_genre_handler(callback_query.message, state, args[2].strip())
    else:
        await packs_menu(callback_query.message, state)


@dp.callback_query_handler(lambda cq: cq.data and cq.data.startswith(PacksCallback.MORE))
async def callback_handler_more_packs(callback_query: types.CallbackQuery):
    fr = int(callback_query.data.split(",")[1])
    packs = await config.storage.get_packs(config.QUERY_LIMIT, fr)
    packs_count = await config.storage.get_packs_count()
    message_packs = '\n'.join([f'{fr + i + 1}) {pack.name}' for i, pack in enumerate(packs)])
    await update_packs_message(callback_query, message_packs, kb.PacksKeyboard.get_ten(
        fr + config.QUERY_LIMIT if fr + config.QUERY_LIMIT < packs_count else None
    ))


@dp.callback_query_handler(lambda cq: cq.data and cq.data == PacksCallback.FILTRED)
async def callback_handler_filtred(callback_query: types.CallbackQuery):
    packs = await config.storage.get_packs(config.QUERY_LIMIT)
    message_packs = '\n'.join([f'{i + 1}) {pack.name}' for i, pack in enumerate(packs)])
    packs_count = await config.storage.get_packs_count()
    await update_packs_message(
        callback_query,
        message_packs,
        kb.PacksKeyboard.get_ten(next_packs=0 + config.QUERY_LIMIT if 0 + config.QUERY_LIMIT < packs_count else None)
    )


@dp.callback_query_handler(lambda cq: cq.data and cq.data == PacksCallback.TEN)
async def callback_handler_ten(callback_query: types.CallbackQuery):
    packs = await config.storage.get_packs_by_rate(config.QUERY_RATE_LIMIT)
    message_packs = '\n'.join([f'{i + 1}) {pack.name}' for i, pack in enumerate(packs)])
    await update_packs_message(
        callback_query,
        ms_packs=message_packs,
        keyboard=kb.PacksKeyboard.get_filtred()
    )


async def update_packs_message(cq, ms_packs, keyboard):
    await config.bot.edit_message_text(ms_packs, cq.message.chat.id, cq.message.message_id, reply_markup=keyboard)
