import discord
from discord.ext import commands

class Moderation(commands.Cog):
    '''A group of commands used for moderation of your discord, \n
     server use !help command_name to get help with a specific command and 
     see what level of athority you need to use it.'''
    pass

    def __init__(self, bot):
        self.bot = bot
        self.guilds = bot.guilds

        for guild in self.guilds:
            with open(f'data/{guild.id}/tickets.json') as file:

    @commands.command()
    async def add_ticket(self, ctx, guild_id, type, title, *msg):
        '''This command creates a new issue ticket, please use it in a dm channel. \n
           use the command like this: !add_ticket "guild_id" "type" "title" "Your issue long answer" \n
           please put your title and message in quotes and keep your title short, and be as discriptive as posible \n 
           if your issue is with me(the bot) please put "bot" in type \n
           if your issue is a guild issue please put "guild" in type \n
           you can get the guild id from the direct command'''
        user = ctx.author
        user_id = ctx.author.id
        if len(msg) > 1:
            joined = ''
            msg = msg.join()
        else:
            msg = msg[0]
        
        if type.lower() == 'bot':
            #add to bot database
            #send message to me that a ticket has been added
        
        elif type.lower() == 'guild' or type.lower() == 'server':
            #check if bot is in that server
            #check if user is in that server
            #find correct server database
            #add data to server database
            # send message to server staff

        await ctx.channel.send(f'{guild_id},{type},{title},{msg}')
        

    @commands.command()
    async def direct(self, ctx):
        user = ctx.author
        guild_name = ctx.guild.name
        guild_id = ctx.guild.id
        await user.send(f'Hello {user.display_name}, we are coming from {guild_name}. \n The guild id for issues is: {guild_id}.')

def setup(bot):
    bot.add_cog(Moderation(bot))