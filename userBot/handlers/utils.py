import re

from userBot import config
from userBot.keyboards import button as bt


async def send_message_to_u(chat_id, message, rp):
    return await config.bot.send_message(
        chat_id,
        message,
        reply_markup=rp
    )


def lambda_for_packs_genres(message):
    return message.text and (
            message.text == bt.GenresButtons.HIP_HOP or
            message.text == bt.GenresButtons.RNB or
            message.text == bt.GenresButtons.ROCK or
            message.text == bt.GenresButtons.HOUSE_TECHNO or
            message.text == bt.GenresButtons.POP or
            message.text == bt.GenresButtons.DANCEHALL_AFRO or
            message.text == bt.GenresButtons.MORE)


def lambda_for_sounds(message):
    return message.text and (
            message.text == bt.MenuButtons.SOUNDS or
            message.text == bt.CommonButtons.BACK_TO_SOUNDS)


async def to_sounds_filter(mes, text, board):
    await config.bot.send_message(mes.chat.id, text, reply_markup=board())


def lambda_sound(message):
    return message.text and (
            message.text[:-1] == bt.MelodiesButtons.GUITARS or
            message.text[:-1] == bt.MelodiesButtons.KEYS or
            message.text == bt.MelodiesButtons.SYNTH or
            message.text[:-1] == bt.MelodiesButtons.VOCALS or
            message.text[:-1] == bt.MelodiesButtons.SAMPLES or
            message.text[:-1] == bt.MelodiesButtons.STRINGS or
            message.text[:-1] == bt.DrumsButtons.KICKS or
            message.text[:-1] == bt.DrumsButtons.SNARES or
            message.text[:-1] == bt.DrumsButtons.HATS or
            message.text[:-1] == bt.DrumsButtons.CLAPS or
            message.text[:-1] == bt.DrumsButtons.CYMBALS or
            message.text == bt.DrumsButtons.BASS or
            message.text[:-1] == bt.DrumsButtons.PERCUSSIONS or
            message.text == bt.DrumsButtons.FX or
            message.text[:-1] == bt.DrumsButtons.LOOPS or
            message.text == bt.DrumsButtons.MORE)


def parse_max_index(menu):
    max_index = 0
    for row in menu:
        var = re.findall(r'(\d+)', row)[0]
        max_index = int(var) if max_index < int(var) else max_index
    return max_index


def get_menu_nums(menu):
    return [re.findall(r'(\d+)', row)[0] for row in menu]


def parse_name_fr_menu(menu, pack_id):
    for row in menu:
        args = row.split(')')
        if int(args[0]) == pack_id:
            return args[1]
