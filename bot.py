import os
import math
import logging
import discord
import json

logging.basicConfig(level=logging.INFO)


TOKEN = os.getenv('DISCTOKEN')

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Im here to help !help'))
    print(f"{client.user} is ready for use!")

#----------------------------------------------------------------------------------------------------------------------------------------------------
# Edit Handler -- Listens for messages that have been edited and logs them
#----------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_message_edit(before,after):
    user = before.author
    channel = before.channel
    guild = before.guild

    if guild:
        path = f'chatlogs/{guild.id}_{guild.name}.txt'
        with open(path, 'a+') as f:
            print(f'{user.name} edited a message: {before.content} ---> {after.content}')

    pass

#----------------------------------------------------------------------------------------------------------------------------------------------------
# Message Handler -- Listens for messages
#----------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_message(message):
    user = message.author
    channel_name = message.channel.name 
    channel_id = message.channel.id
    content = message.content
    guild = message.guild
    
    #if message.author == client.user:
    #    path = f'chatlogs/{guild.name}_Virgo.txt'
    #    with open(path, 'a+') as s:
    #        print(f'{message.created_at} : {message.channel.name} : {message.content}' ,file = s)
    #    return

#----------------------------------------------------------------------------------------------------------------------------------------------------
# Chat logger -- logs all messages
#----------------------------------------------------------------------------------------------------------------------------------------------------
 
    if guild:
        path = f'chatlogs/{guild.id}_{guild.name}.txt'
        with open(path, 'a+') as f:
            print(f'{message.created_at} : {user} : {channel_name or channel_id} : {message.content}',file = f)



#----------------------------------------------------------------------------------------------------------------------------------------------------
# Chat Level System -- Listens for messages
#
#   Rebuilt
#----------------------------------------------------------------------------------------------------------------------------------------------------

    with open('data/levels.json', 'r') as d:
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
                with open('data/levels.json', 'w') as file:
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
                with open('data/levels.json', 'w') as file:
                    users['user'].append(json_string)
                    d.seek(0)
                    json.dump(users, file, indent=4)
                    print('success')
                    break

#----------------------------------------------------------------------------------------------------------------------------------------------------
# Check Level -- Check your level in the chat
#----------------------------------------------------------------------------------------------------------------------------------------------------
#  
    if message.content.startswith('!stats'):
        with open('data/levels.json','r') as file_data:
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
                    await message.channel.send(embed=stats)
                    
        


#----------------------------------------------------------------------------------------------------------------------------------------------------
# Hello Command -- Small description of the bot and where to report bugs
#----------------------------------------------------------------------------------------------------------------------------------------------------
    if message.content.startswith('!hello'):
        print(f'{user} has used the hello command')
        hello_msg = f"Hello! {user.mention}! My name is Virgo, I am a utility bot specialy made for The Vibe Checkers. I am currently in development so if you notice any bugs or glitches please report them to <@!241296650650255372>"
        await message.channel.send(hello_msg)


#----------------------------------------------------------------------------------------------------------------------------------------------------
# Activity Command -- Shows the song user is listening to or game they are playing
#----------------------------------------------------------------------------------------------------------------------------------------------------
    if message.content.startswith('!activity'):
        print(f'{user} has used the activity command')
        if str(user.activity) == 'Spotify':
            state = user.activity.type
            song  = user.activity.title
            artist  = user.activity.artist
            msg = f"{user.mention} you are listening to {song} by {artist} "
            await message.reply(msg)
        
        elif str(user.activity) == 'Game':
            state = user.activity.type 
            game = user.activity.name
            msg = f"{user.mention} you are playing {game}"
            await message.reply(msg)

        elif user.activity == None:
            msg = f"{user.mention} you are doing nothing..... BORING!!!"
            print(user.activity)
            await message.reply(msg)

        else:
            pass


#--------------------------------------------------------------------------
# Help Command
#--------------------------------------------------------------------------         
    if message.content.startswith('!help'):
        print(f'{user} has used the help command')
        msg = '''--List of Commands--
!hello -Virgo will say hello!
!activity -shows your discord activity
!selfhelp covid - a link to a self help resourse in regards to Covid
!selfhelp apps - a link to some usefull self help apps for Apple and Android
!yesnt - No but Yes?
!chomp - chomp
'''
        await message.channel.send(msg)  


#--------------------------------------------------------------------------
# yesnt Command
#--------------------------------------------------------------------------         
    if message.content.startswith('!yesnt'):
        print(f'{user} has used the yesnt command')
        msg = '''yes    yes  yes yes yes
yes yes  yes yes    yes
yes yes yes  yes    yes
yes  yesyes yes    yes
yes    yes  yes yes yes
'''
        await message.channel.send(msg)

#--------------------------------------------------------------------------
# Chomp Gif -- Sends a Gif of Chomp
#--------------------------------------------------------------------------         
    if message.content.startswith('!chomp'):
        msg = 'Chomp'
        img = discord.File('assets/anime-bite.gif')

        await message.channel.send(content = msg, file = img)

#--------------------------------------------------------------------------
# Mmmm Gif -- Sends a gif of sully Mmmm
#-------------------------------------------------------------------------- 
    if message.content.startswith('!oof'):
        img = discord.File('assets/oof-scared.gif')

        await message.channel.send(file = img)
#--------------------------------------------------------------------------
# Self Help Command -- Shows self help link 
#--------------------------------------------------------------------------         
        
    if message.content.startswith('!selfhelp'):
        print(f'{user} has used the self help command')
        
        if 'covid' in message.content.lower():
            msg = 'Mental health in regards to Covid 19 ---- https://www.camh.ca/en/health-info/mental-health-and-covid-19'
        
        elif 'apps' in message.content.lower():
            msg = 'Coe College list of helpfull apps ----- https://www.coe.edu/student-life/student-life-resources/health-wellness/mental-health-counseling/self-help-resources'

        elif 'anxiety' in message.content.lower():
            msg = 'Helpfull resources for Anxiety ----- https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/self-care/'
        
        else:
            msg = 'This command takes a second input, please use !help to see use cases!'
        
        
        await message.channel.send(msg)
        
    else:
        pass
    
    
#----------------------------------------------------------------------------------------------------------------------------------------------------
# Voice State Listener -- Listens for voice updates such as join channel, leave channel, mute, video settings Exc.
#----------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == None:
    
        if after.channel == None:
            pass


#----------------------------------------------------------------------------------------------------------------------------------------------------
# Smoke Sesh -- alerts @Stoners when someone starts a Sesh -- Vibe Checkers Exclusive
#----------------------------------------------------------------------------------------------------------------------------------------------------
        elif  str(after.channel) == 'Smoke Sesh':
            a_channel = after.channel 
            txt_channel = client.get_channel(853860579291037746)
            members = len(a_channel.members)
            print(f'{member} has entered the Sesh with {members - 1} other users')
            msg = f'{member.mention} has started a Sesh! Feel free to stop in <@&919808899752816650>'
            if members == 1:
                await txt_channel.send(msg)
        
        else:
            pass


#----------------------------------------------------------------------------------------------------------------------------------------------------
# Welcome Messages -- listens for new users and welcomes them to the guild
#----------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    guild = member.guild
    print(f'{member} has joined the Guild')
    if guild.system_channel != None:
        w_message = f'Welcome {member.mention} to {guild.name}! We hope you enjoy your stay!'
        await guild.system_channel.send(w_message)


#----------------------------------------------------------------------------------------------------------------------------------------------------
# User Left Messages -- listens for users to leave the server permenantly and sends a message -- WIP
#----------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_leave(member):
    guild = client.guild
    print(f'{member} has left the Guild')
    if guild.system_channel != None:
        l_message = f'{member.name} has left us! how sad :sob:'
        await guild.system_channel.send(l_message)
    
    else:
        path = f'chatlogs/{guild.id}_{guild.name}.txt'
        with open(path, 'a+') as f:
            print(f'{member.name} has left us!', file = f )


client.run(TOKEN)