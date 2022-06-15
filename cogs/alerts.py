from ssl import CHANNEL_BINDING_TYPES
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
    async def stop_water(self, ctx):
        self.water.stop()
        await ctx.channel.send('Water stopped')

    @commands.command()
    async def start_water(self, ctx):
        self.water.start()
        await ctx.channel.send('Here comes the rain!')
    
    #Change Loop time
    @commands.command()
    async def change_loop(self,ctx):#12 char
        message = ctx.message
        channel = ctx.channel

        message = message.content[12:]
        if message != '':
            msgsplit = message.split()
            hour=int(msgsplit[0])
            minute=int(msgsplit[1])
            sec=int(msgsplit[2])
            self.water.change_interval(hours=hour, minutes=minute, seconds=sec)
            await channel.send(f'Interval changed to {hour} hours, {minute} minutes, and {sec} seconds')
        else:
            await channel.send('Enter hour min sec')

        
    @tasks.loop(seconds = 54)
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
