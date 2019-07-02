from __future__ import annotations
from discord.ext import commands
from base.struct import Config
import json


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='.',
            description='Discord bot leveling system example.'
        )

        with open('config.json', 'r') as f:
            self.cfg = Config(json.loads(f.read()))

        self.cog_list = ['cogs.leveling']
        for cog in self.cog_list:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f'Error occured while cog "{cog}" was loaded.\n{e}')

    def startup(self):
        self.run(self.cfg.bot_token)


if __name__ == '__main__':
    Bot().startup()
