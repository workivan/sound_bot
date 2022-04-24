import asyncpg

from userBot.storage.Pack import Pack
from userBot.storage.Payment import Payment
from userBot.storage.Sound import Sound
from userBot.storage.User import User


class Storage:
    connection = None

    async def init(self, db_url):
        self.connection = await asyncpg.connect(db_url)

    async def update_sub(self, chat_id, period, now='CURRENT_DATE'):
        await self.connection.execute(
            f"""update "user" set subscription_to={now} + {period} where chat_id={chat_id}""")

    async def get_user(self, chat_id):
        row = await self.connection.fetchrow(f"""select * from "user" where chat_id={chat_id}""")
        return User(row) if row is not None else None

    async def create_user(self, chat_id, username, deep_link=""):
        await self.connection.execute(f"""insert into "user" values({chat_id}, '{username}', '{deep_link}')""")
        return await self.get_user(chat_id)

    async def get_packs(self, limit, fr=0):
        rows = await self.connection.fetch(
            f"""select * from "pack" where cost=0 order by uploaded  DESC  offset {fr} limit {limit}""")
        return [Pack(row) for row in rows]

    async def get_packs_by_rate(self, limit):
        rows = await self.connection.fetch(f"""select * from "pack" where cost=0 order by rate DESC limit {limit}""")
        return [Pack(row) for row in rows]

    async def set_pay(self, chat_id, product, cost):
        await self.connection.execute(
            f"""insert into "payment" (chat_id, product, cost) values ({int(chat_id)}, '{product}', {int(cost)})""")

    async def get_pay_by_user_and_product(self, chat_id, product):
        row = await self.connection.fetchrow(
            f"""select * from "payment" where chat_id={int(chat_id)} and product='{product}'""")
        if row:
            return Payment(row)

    async def get_pack_with_id(self, pack_id, order):
        row = await self.connection.fetchrow(
            f"""select * from "pack" order by {order} DESC offset {int(pack_id) - 1} limit 2""")
        # Здесь почему нужно limit 2 чтобы получить pack_id + 1 запись
        return Pack(row)

    async def get_packs_count(self):
        row = await self.connection.fetchrow('select count(*) from "pack" where cost=0')
        return row["count"]

    async def get_pack_by_name(self, pack_name):
        row = await self.connection.fetchrow(f"""select * from "pack" where full_name='{pack_name}'""")
        return Pack(row)

    # звуки
    async def get_sounds_by_type(self, sound_type, limit, fr=0):
        rows = await self.connection.fetch(
            f"""select * from "sound" where sound_type='{sound_type}' offset {fr} limit {limit}""")
        return [Sound(row) for row in rows]

    async def get_sound_by_name(self, name):
        row = await self.connection.fetchrow(f""" select * from "sound" where name='{name}'""")
        return Sound(row)

    async def get_sounds_count_by_type(self, type_id):
        row = await self.connection.fetchrow(f"""select count(*) from "sound" where sound_type='{type_id}'""")
        return row["count"]

    # sub
    async def is_sub(self, chat_id):
        row = await self.connection.fetchrow(f"""select * from""")

    # genres
    async def get_packs_by_genre(self, genre):
        rows = await self.connection.fetch(f"""select * from "pack" where genre='{genre}' """)
        return [Pack(row) for row in rows]

    async def get_pack_by_genre(self, pack_id, genre):
        row = await self.connection.fetchrow(
            f"""select * from "pack" where genre='{genre}' offset {int(pack_id) - 1} limit 2""")
        return Pack(row)

    async def get_exclusive_packs(self):
        rows = await self.connection.fetch(f"""select * from "pack" where cost > 0""")
        return [Pack(row) for row in rows]
