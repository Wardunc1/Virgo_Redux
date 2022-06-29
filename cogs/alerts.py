import time
import discord 
from discord.ext import tasks
from discord.ext import commands

class Alerts(commands.Cog):
    def __init__(self, bot):
        self.bot=bot 
        self.guilds = self.bot.guilds
        self.starttime = 9
        self.endtime = 21
        self.water.start()

    @commands.command()
    async def change_start(self,ctx, arg):
        '''Changes the time that the bot starts sending alerts || !change_start Hr'''
        if arg != None:
            if int(arg) < self.endtime:
                self.starttime = int(arg)
                await ctx.channel.send(f'Start time has been changed to {self.starttime}:00')

            elif int(arg) >= self.endtime:
                await ctx.channel.send(f'Start time must be earlier than the end time {self.endtime}:00')
        
        else:
            await ctx.message.send('Please enter the hour you would like the alerts to send')
        

    
    @commands.command()
    async def change_end(self,ctx,arg):
        '''Changes the time that the bot stops sending alerts || !change_end Hr'''
        if arg != None:
            if int(arg) < int(self.starttime):
                self.endtime = int(arg)
                await ctx.channel.send(f'End time changed to {self.endtime}:00')
            
            elif int(arg) >= int(self.starttime):
                await ctx.channel.send(f'End time must be after start time {self.starttime}:00')
        else:
            await ctx.channel.send('Please enter the hour you would like alerts to stop')
        pass

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
        '''!change_loop h m s \n \nChanges the interval between water messages  \nRemember to use spaces!'''
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

        
    @tasks.loop(hours = 3, seconds = 54)
    async def water(self):
        now = time.localtime()
        if now.tm_hour > self.endtime:
            pass

        if now.tm_hour < self.starttime:
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
