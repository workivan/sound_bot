import re
import shutil

from typing import List

from userBot import config
from userBot.handlers.utils import parse_max_index, parse_name_fr_menu
from userBot.keyboards import message as msg, keyboard as kb
from userBot.services.upload_service import Uploader


async def pack_by_genre_handler(message, state, genre=None):
    packs = await config.storage.get_packs_by_genre(genre if genre else message.text.lower())
    if len(packs) > 0:
        message_packs = '\n'.join([f'{i + 1}) {pack.name}' for i, pack in enumerate(packs)])

        await config.bot.send_message(
            message.chat.id,
            message_packs,
        )

        async with state.proxy() as proxy:
            proxy['GENRES'] = True
            proxy["VIP"] = False
    else:
        await config.bot.send_message(
            message.chat.id,
            msg.PACKS_GENRES_EMPTY
        )


async def exclusive_packs(message, state):
    packs = await config.storage.get_exclusive_packs()
    if len(packs) > 0:
        message_packs = '\n'.join([f'{i + 1}) {pack.name}' for i, pack in enumerate(packs)])

        await config.bot.send_message(
            message.chat.id,
            msg.WELCOME_PACKS_MESSAGE
        )
        await config.bot.send_message(
            message.chat.id,
            message_packs
        )
        async with state.proxy() as proxy:
            proxy['GENRES'] = False
            proxy['VIP'] = True
    else:
        await config.bot.send_message(
            message.chat.id,
            msg.EXCLUSIVE_CONTENT_EMPTY
        )


async def pack_by_menu(message, fr=0):
    packs = await config.storage.get_packs(config.QUERY_LIMIT)
    packs_count = await config.storage.get_packs_count()

    message_packs = '\n'.join(
        [f'{i + 1}) {pack.name}' for i, pack in enumerate(packs)])

    await config.bot.send_message(
        message.chat.id,
        msg.WELCOME_PACKS_MESSAGE,
    )

    await config.bot.send_message(
        message.chat.id,
        message_packs,
        reply_markup=kb.PacksKeyboard.get_ten(
            fr + config.QUERY_LIMIT if fr + config.QUERY_LIMIT < packs_count else None
        )
    )


async def reply_for_packs(message, reply_text, state):
    digits_from_user = re.findall(r'(\d+)', message.text)
    if len(digits_from_user) == 0:
        return
    pack_id = int(digits_from_user[0])

    menu: List[str] = re.findall('\d+\)[a-z ]+', reply_text)
    if pack_id <= 0 or pack_id > parse_max_index(menu):
        return

    pack_name = parse_name_fr_menu(menu, pack_id)
    pack_with_id = await config.storage.get_pack_by_name(pack_name.strip())
    await config.bot.send_message(
        message.chat.id,
        msg.DOWNLOAD_PACK_MESSAGE + pack_name
    )

    ogg_files, temp_dir_files = Uploader.upload_sounds_from_pack(pack_with_id)
    for ogg, name in ogg_files:
        async with state.proxy() as proxy:
            if 'VIP' in proxy and not proxy['VIP']:
                await config.bot.send_message(
                    message.chat.id,
                    name
                )
        await config.bot.send_voice(
            message.chat.id,
            voice=open(ogg, 'rb')
        )
    pays = await config.storage.get_pay_by_user_and_product(message.chat.id, pack_name.strip())
    if pays:
        bought = True
    else:
        bought = False

    shutil.rmtree(temp_dir_files, ignore_errors=True)
    async with state.proxy() as proxy:
        if 'VIP' in proxy and proxy['VIP']:
            await config.bot.send_message(
                message.chat.id,
                msg.BUY_PACK,
                reply_markup=kb.PacksKeyboard.get_buy(pack_name, bought)
            )
        elif 'GENRES' in proxy and proxy['GENRES']:
            await config.bot.send_message(
                message.chat.id,
                msg.BUY_PACK,
                reply_markup=kb.PacksKeyboard.get_download_g(pack_name, 'genres', pack_with_id.genre)
            )
        else:
            await config.bot.send_message(
                message.chat.id,
                msg.DOWNLOAD_PACK,
                reply_markup=kb.PacksKeyboard.get_download_g(pack_name, None)
            )
