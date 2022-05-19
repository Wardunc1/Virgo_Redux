import time
import discord 
from discord.ext import tasks
from discord.ext import commands

class Alerts(commands.Cog):
    def __init__(self, bot):
        self.bot=bot 
        self.guilds = self.bot.guilds
        self.water.start()

    @commands.command()
    async def stop_water(self):
        self.water.stop()
    
    @commands.command()
    async def start_water(self):
        self.water.start()
        
    @tasks.loop(hours =1, minutes = 21, seconds = 54)
    async def water(self):
        now = time.localtime()
        if now.tm_hour > 23:
            pass

        if now.tm_hour < 6:
            pass

        else: 
            for guild in self.guilds:
                channels = await guild.fetch_channels()
                done = False
                for channel in channels:
                    if channel.name == 'virgo-bot':
                        content = 'Remember to drink some water and have a stretch!'
                        await channel.send(content)
                        done = True

                    elif done:
                        pass


def setup(bot):
    bot.add_cog(Alerts(bot))
