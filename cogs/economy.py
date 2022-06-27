from operator import contains
import os
import time
import json
import random
import discord
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds = bot.guilds

        for guild in self.guilds:
            
            try:
                #load database
                db = open(f'data/{guild.id}/economy.json')

                if db != None:
                    print('Economy Data Found!')
                
            except Exception as e:
                print(f'{e} :Creating Economy for {guild.name}')
                #creating new data folder for guild
                parent = 'data'
                newdir = f'{guild.id}'
                path = os.path.join(parent,newdir)
                now = time.time()
                now = str(now).split('.')[0]
                try:
                    os.mkdir(path)
                
                except Exception as e:
                    print(e)

                with open(f'data/{guild.id}/economy.json', 'w') as file:
                    jstring = {

                        "user": [
                                {
                                "name": "Filler",
                                "lastwork": f"{now}",
                                "id": "001",
                                "coins": "0",
                                "wins": "0",
                                "losses": "0",
                                }
                        ]}
                    json.dump(jstring, file, indent=5)
                    print('Economy data created')
    
    @commands.command()
    async def work(self, ctx):
        
        user = ctx.author
        channel = ctx.channel
        guild = ctx.guild
        job = 'job'
        wage = min(random.randrange(10, 300, 5), random.randrange(10, 300, 5))
        now = time.time()
        now = str(now).split('.')[0]
        with open(f'data/{guild.id}/economy.json', 'r') as d:
            users = json.load(d)
            print('doc opened')
            counter = 0
            for u in users['user']:
                counter+= 1
                
                if str(user.id) == u['id']:  
                    if int(now) >= int(u['lastwork'])+86400:
                        lastwork = now
                        coins = int(u['coins']) + wage
                        with open(f'data/{guild.id}/economy.json', 'w') as file:
                            u['lastwork'] = lastwork
                            u['coins'] = coins
                            json.dump(users, file, indent=5)
                            await channel.send(f'{user.mention} worked {job} and made {wage} coins!')

                    elif int(now) <= int(u['lastwork'])+86400:
                        await channel.send(f'{user.mention}, You can only work once every 24 hours')

                elif counter == len(users['user']):
                    jstring = {
                                "name": f"{str(user.name)}",
                                "lastwork": f'{now}',
                                "id": f"{str(user.id)}",
                                "coins": "150",
                                "wins": "0",
                                "losses": "0",
                                }
                    with open(f'data/{guild.id}/economy.json', 'w') as file:
                        users['user'].append(jstring)
                        d.seek(0)
                        json.dump(users, file, indent=5)
                        print('user added')
                        await channel.send(f'{user.mention} worked {job} and made 150 coins!')
                    

    @commands.command()
    async def wallet(self, ctx, *arg):

        user = ctx.author
        channel = ctx.channel
        guild = ctx.guild
        if arg == ():
            with open(f'data/{guild.id}/economy.json', 'r') as f:
                users = json.load(f)
                for u in users['user']:
                    if str(user.id) == u['id']:
                        coins = u['coins']
                        lastwork = time.localtime(int(u['lastwork']))
                        await channel.send(f'{user.mention},You currently have {coins} coins and last worked {time.asctime(lastwork)}')
                        



            print('no args')
        elif len(arg) > 1:
            await channel.send('Please enter one name')

        else:
            #Find user and print wallet
            with open(f'data/{guild.id}/economy.json', 'r') as file:
                users = json.load(file)

                for u in users['user']:
                    if u['name'].lower() == arg[0].lower():
                        coins = u['coins']
                        uname = u['name']
                        lastwork = time.localtime(int(u['lastwork']))
                        await channel.send(f'{uname} has {coins} coins and last worked on {lastwork}')

                        print('user found')
                    else:
                        await channel.send('User not found.')       

    def blackjack():
        pass

    def roulett():
        pass



def setup(bot):
    bot.add_cog(Economy(bot))