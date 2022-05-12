import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds = bot.guilds

        for guild in self.guilds:
            #Checking For Logging File
            try:
                with open(f'chatlogs/{guild.id}_{guild.name}.txt','r') as lbd:
                    print(lbd)
                    if lbd != None:
                        print('Chat Log Found!')

            except:
                print('Creating Chat Log!')
                with open(f'chatlogs/{guild.id}_{guild.name}.txt','w') as f:
                    print(f' Date   :  UserName  :  Channel  :  Content  ' ,file = f)

    @commands.Cog.listener()
    async def on_message(self, msg):
        user = msg.author
        channel_name = msg.channel.name
        channel_id = msg.channel.id
        guild = msg.guild
        
        path = f'chatlogs/{guild.id}_{guild.name}.txt'
        with open(path, 'a+') as f:
            print(f'{msg.created_at} : {user} : {channel_name or channel_id} : {msg.content}',file = f)






def setup(bot):
    bot.add_cog(Logging(bot))