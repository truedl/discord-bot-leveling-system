from __future__ import annotations
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import asyncpg


class Database:
    def __init__(self, loop, user: str, password: str) -> None:
        self.user = user
        self.password = password
        loop.create_task(self.connect())

    async def connect(self) -> None:
        self.conn = await asyncpg.connect(user=self.user, password=self.password, host='127.0.0.1')
        exists = await self.conn.fetch('SELECT datname FROM pg_catalog.pg_database WHERE datname=\'discordleveling\'')        
        if not exists:
            await self.conn.fetch('CREATE DATABASE discordleveling')
        await self.conn.close()
        self.conn = await asyncpg.connect(user=self.user, password=self.password, database='discordleveling', host='127.0.0.1')
        await self.conn.fetch('CREATE TABLE IF NOT EXISTS users (id TEXT NOT NULL, rank INT NOT NULL, xp INT NOT NULL)')

    async def fetch(self, sql: str) -> list:
        return await self.conn.fetch(sql)


class Rank:
    def __init__(self) -> None:
        self.font = ImageFont.truetype('arialbd.ttf', 28)
        self.medium_font = ImageFont.truetype('arialbd.ttf', 22)
        self.small_font = ImageFont.truetype('arialbd.ttf', 16)

    def draw(self, user: str, rank: str, xp: str, profile_bytes: BytesIO) -> BytesIO:
        profile_bytes = Image.open(profile_bytes)
        im = Image.new('RGBA', (400, 148), (44, 44, 44, 255))

        im_draw = ImageDraw.Draw(im)
        im_draw.text((154, 5), user, font=self.font, fill=(255, 255, 255, 255))

        rank_text = f'RANK {rank}'
        im_draw.text((154, 37), rank_text, font=self.medium_font, fill=(255, 255, 255, 255))

        needed_xp = self.neededxp(rank)
        xp_text = f'{xp}/{needed_xp}'
        im_draw.text((154, 62), xp_text, font=self.small_font, fill=(255, 255, 255, 255))

        im_draw.rectangle((174, 95, 374, 125), fill=(64, 64, 64, 255))
        im_draw.rectangle((174, 95, 174+(int(xp/needed_xp*100))*2, 125), fill=(221, 221, 221, 255))

        im_draw.rectangle((0, 0, 148, 148), fill=(255, 255, 255, 255))
        im.paste(profile_bytes, (10, 10))

        buffer = BytesIO()
        im.save(buffer, 'png')
        buffer.seek(0)

        return buffer

    @staticmethod
    def neededxp(level: str) -> int:
        return 100+level*80


class Utilities:
    def __init__(self):
        self.database = Database
        self.rankcard = Rank()


utilities = Utilities()
