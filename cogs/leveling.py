from __future__ import annotations
from asyncio import sleep as asyncsleep
from base.utilities import utilities
from discord.ext import commands
from random import randint
from io import BytesIO
from discord import File as dFile
from discord import Member as dMember
import aiohttp


class Leveling(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.db = utilities.database(self.bot.loop, self.bot.cfg.postgresql_user, self.bot.cfg.postgresql_password)
        self.brake = []

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author.id not in self.brake:
            if not await self.db.fetch(f'SELECT * FROM users WHERE id=\'{message.author.id}\''):
                await self.db.fetch(f'INSERT INTO users (id, rank, xp) VALUES (\'{message.author.id}\', \'0\', \'0\')')
                current_xp = 0

            else:
                result = await self.db.fetch(f'SELECT rank, xp FROM users WHERE id=\'{message.author.id}\'')
                current_xp = result[0][1] + randint(self.bot.cfg.min_message_xp, self.bot.cfg.max_message_xp)

                if current_xp >= utilities.rankcard.neededxp(result[0][0]):
                    await self.db.fetch(f'UPDATE users SET rank=\'{result[0][0]+1}\', xp=\'0\' WHERE id=\'{message.author.id}\'')
                else:
                    await self.db.fetch(f'UPDATE users SET xp=\'{current_xp}\' WHERE id=\'{message.author.id}\'')

                self.brake.append(message.author.id)
                await asyncsleep(randint(15, 25))
                self.brake.remove(message.author.id)

    @commands.is_owner()
    @commands.command()
    async def tsql(self, ctx, *, sql: str) -> None:
        output = await self.db.fetch(sql)
        await ctx.send(f'```{output}```')

    @commands.command()
    async def rank(self, ctx, member: dMember=None) -> None:
        if member:
            uMember = member
        else:
            uMember = ctx.author
        result = await self.db.fetch(f'SELECT rank, xp FROM users WHERE id=\'{uMember.id}\'')
        if result:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{uMember.avatar_url}?size=128') as resp:
                    profile_bytes = await resp.read()

            buffer = utilities.rankcard.draw(str(uMember), result[0][0], result[0][1], BytesIO(profile_bytes))

            await ctx.send(file=dFile(fp=buffer, filename='rank_card.png'))
        else:
            await ctx.send(f'{uMember.mention}, you don\'t received xp yet.')


def setup(bot) -> None:
    bot.add_cog(Leveling(bot))
