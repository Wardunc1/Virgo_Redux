import logging
import os
import json
import discord
import discord.ext
from discord.ext import commands


TOKEN = os.getenv('DISCTOKEN')

intents=discord.Intents.default()
intents.members   = True
intents.presences = True
intents.messages  = True

class Virgo_Bot(commands.Bot):
    def __init__(self, command_prefix='!',self_bot=False,*args,**kwargs):
            
        super().__init__(command_prefix='!', *args, **kwargs)

    async def on_ready(self):
        print('Loading Cogs')
        for cog in os.listdir('cogs'):
            if cog[:2] == '__' :
                pass
            else:
                try:
                    self.load_extension(f'cogs.{cog[:-3]}')
                    print(f'Loaded {cog[:-3]}')
                except Exception as e:
                    print(f'There was an error loading {cog[:-3]} \n {e}')
        
        await self.change_presence(activity=discord.Game(name='Im here to help !help'))
        print(f"{self.user} is ready for use!")    



bot = Virgo_Bot('!', False)
bot.run(TOKEN)