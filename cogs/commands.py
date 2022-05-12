import discord
from discord.ext import commands

class Chat_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name ='hello')
    async def hello(self, msg):
        user = msg.author

        print(f'{user} has used the hello command')
        hello_msg = f"Hello! {user.mention}! My name is Virgo, I am a utility bot specialy made for The Vibe Checkers. I am currently in development so if you notice any bugs or glitches please report them to <@!241296650650255372>"
        await msg.channel.send(hello_msg)
    
    @commands.command()
    async def activity(self, msg):
        '''This command shows your activity as shown on Discord'''
        user = msg.author
        print(f'{user} has used the activity command')
        if str(user.activity) == 'Spotify':
            state = user.activity.type
            song  = user.activity.title
            artist  = user.activity.artist
            st = f"{user.mention} you are listening to {song} by {artist} "
            await msg.reply(st)
        
        elif str(user.activity) == 'Game':
            state = user.activity.type 
            game = user.activity.name
            st = f"{user.mention} you are playing {game}"
            await msg.reply(st)

        elif user.activity == None:
            st = f"{user.mention} you are doing nothing..... BORING!!!"
            print(user.activity)
            await msg.reply(st)

        else:
            pass

    @commands.command()
    async def yesnt(self, msg):
        user = msg.author
        print(f'{user} has used the yesnt command')
        st = '''yes    yes  yes yes yes
yes yes  yes yes    yes
yes yes yes  yes    yes
yes  yesyes yes    yes
yes    yes  yes yes yes
'''
        await msg.channel.send(st)

    @commands.command()
    async def chomp(self, msg):
        content = 'Chomp'
        img = discord.File('assets/anime-bite.gif')

        await msg.channel.send(content = content, file = img)

    @commands.command()
    async def oof(sels, msg):
        img = discord.File('assets/oof-scared.gif')

        await msg.channel.send(file = img)



    @commands.command()
    async def selfhelp(self, msg):
        '''This command takes a second input! \n covid for help with covid related issues \n apps will show a list of selfhelp apps \n anxiety will show some resources for anxiety and panic attacks \n Feel free to make more suggestions!'''
        print(f'{msg.author.name} has used the self help command')
        
        if 'covid' in msg.message.content.lower():
            content = 'Mental health in regards to Covid 19 ---- https://www.camh.ca/en/health-info/mental-health-and-covid-19'
        
        elif 'apps' in msg.message.content.lower():
            content = 'Coe College list of helpfull apps ----- https://www.coe.edu/student-life/student-life-resources/health-wellness/mental-health-counseling/self-help-resources'

        elif 'anxiety' in msg.message.content.lower():
            content = 'Helpfull resources for Anxiety ----- https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/self-care/'
        
        else:
            content = 'This command takes a second input, please use !help to see use cases!'
        
        
        await msg.channel.send(content)
        


    

def setup(bot):
    bot.add_cog(Chat_commands(bot))