import math
import json
import discord
from discord.ext import commands

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        self.guilds = self.bot.guilds

        for guild in self.guilds:
            #check for level file
            try:
                ldb = open(f'data/{guild.id}/levels.json', 'r+')

                if ldb != None:
                    print('Level Data Found!')

            except:
                print('Creating Level data!')
                with open(f'data/{guild.id}/levels.json','w') as file:
                    jstring = {

                    "user": [
                            {
                            "name": "Filler",
                            "id": "001",
                            "xp": "10",
                            "level": "1"
                            }
                    ]}
                    json.dump(jstring, file, indent=4)
                    print('Levels data created')

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        channel_name = message.channel.name 
        channel_id = message.channel.id
        content = message.content
        guild = message.guild

    
        with open(f'data/{guild.id}/levels.json', 'r') as d:
            users = json.load(d)
            print('doc opened')
            counter = 0
            for u in users['user']:
                counter += 1
                if str(user.id) == u['id']:
                    xp = int(u['xp']) + 5
                    level = int(math.sqrt(xp)/5)
                    if level > int(u['level']):
                        u['level'] = str(level)
                        embed = discord.Embed(title=f'{user.display_name} has leveled up to {level}!!')
                        await message.channel.send(f'{user.mention}', embed=embed)
                    u['xp'] = str(xp)
                    with open(f'data/{guild.id}/levels.json', 'w') as file:
                        d.seek(0)
                        json.dump(users,file,indent=4)
                        print(f'{u} found!')
                        break
                    
                elif counter == len(users['user']):
                    json_string = {
                    'name' : '{}'.format(str(user.name)),
                    'id' : '{}'.format(str(user.id)),
                    'xp' : '{}'.format(str(5)),
                    'level':'{}'.format(str(1))
                    }
                    with open(f'data/{guild.id}/levels.json', 'w') as file:
                        users['user'].append(json_string)
                        d.seek(0)
                        json.dump(users, file, indent=4)
                        print('success')
                        break

    @commands.command(name='stats')
    async def check_level(self, msg):
        user = msg.author
        guild = user.guild
        
        with open(f'data/{guild.id}/levels.json','r') as file_data:
            file = json.load(file_data)
            for u in file['user']:
                if str(user.id) == u['id']:
                    xp = int(u['xp'])
                    level = int(math.sqrt(xp)/5)
                    if level < 1:
                        level = 1

                    stats = discord.Embed(title=f"{user.name}'s Stats!")
                    stats.add_field(name='Level:', value=f'{level}', inline=False)
                    stats.add_field(name='Exp:', value=f'{xp}', inline=True)
                    await msg.channel.send(embed=stats)

def setup(bot):
    bot.add_cog(Leveling(bot))



