import os
import time
import json
import random
import discord
from asyncio import TimeoutError
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds = bot.guilds
        self.suits = ['D','S','C','H']
        self.cards = [ 'A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.unicode = [b'\u1f0b1',b'\u1f0b2',b'\u1f0b3',b'\u1f0b4',
                        b'\u1f0b5',b'\u1f0b6',b'\u1f0b7',b'\u1f0b8',
                        b'\u1f0b9',b'\u1f0ba',b'\u1f0bb',b'\u1f0bd',
                        b'\u1f0be',b'\u1f0a1',b'\u1f0a2',b'\u1f0a3',
                        b'\u1f0a5',b'\u1f0a6',b'\u1f0a7',b'\u1f0a8',
                        b'\u1f0a9',b'\u1f0aa',b'\u1f0ab',b'\u1f0ad',
                        b'\u1f0ae',b'\u1f0a4',b'\u1f0c1',b'\u1f0c2',
                        b'\u1f0c3',b'\u1f0c4',b'\u1f0c5',b'\u1f0c6',
                        b'\u1f0c7',b'\u1f0c8',b'\u1f0c9',b'\u1f0ca',
                        b'\u1f0cb',b'\u1f0cd',b'\u1f0ce',b'\u1f0d1',
                        b'\u1f0d2',b'\u1f0d3',b'\u1f0d4',b'\u1f0de',
                        b'\u1f0d5',b'\u1f0d6',b'\u1f0d7',b'\u1f0d8',
                        b'\u1f0d9',b'\u1f0da',b'\u1f0db',b'\u1f0dd',
                        ]



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
                if str(user.id) == u['id']:  
                    if int(now) >= int(u['lastwork'])+86400:
                        lastwork = now
                        coins = int(u['coins']) + wage
                        with open(f'data/{guild.id}/economy.json', 'w') as file:
                            u['lastwork'] = lastwork
                            u['coins'] = coins
                            json.dump(users, file, indent=5)
                            d.seek(0)
                            file.seek(0)
                            await channel.send(f'{user.mention} worked {job} and made {wage} coins!')
                            break

                    elif int(now) <= int(u['lastwork'])+86400:
                        d.seek(0)
                        await channel.send(f'{user.mention}, You can only work once every 24 hours')
                        break

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
                        file.seek(0)
                        await channel.send(f'{user.mention} worked {job} and made 150 coins!')
                counter+= 1
                    

    @commands.command()
    async def wallet(self, ctx, *arg):

        user = ctx.author
        channel = ctx.channel
        guild = ctx.guild
        if arg == ():
            with open(f'data/{guild.id}/economy.json', 'r') as f:
                f.seek(0)
                users = json.load(f)
                for u in users['user']:
                    if str(user.id) == u['id']:
                        coins = u['coins']
                        lastwork = time.localtime(int(u['lastwork']))
                        await channel.send(f'{user.mention},You currently have {coins} coins and last worked {time.asctime(lastwork)}')
                    f.seek(0)
                    
                        



            print('no args')
        elif len(arg) > 1:
            await channel.send('Please enter one name')

        else:
            #Find user and print wallet
            with open(f'data/{guild.id}/economy.json', 'r') as file:
                file.seek(0)
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
                file.seek(0)     
    
    
    @commands.command()
    async def blackjack(self, ctx, arg):
        bet = arg
        user = ctx.author
        channel = ctx.channel
        guild = ctx.guild
        _user_id = user.id


        def value(*cards):
            total = 0
            counter = 1
            for card in cards:
                suit = card[0]
                nmb = card[1]
                if nmb in ['J','Q','K']:
                    total += 10
                
                elif nmb == 'A':
                    if counter > 2 and total <= 10 and len(cards) == 2:
                        total += 11
                    
                    elif counter == 1 and len(cards) == 2:
                        total+=  11
                        
                    else:
                        total += 1
                
                elif nmb in [str(x) for x in range(2,10)]:
                    total += int(nmb)
                counter += 1
            
            return total

        
        bet = int(bet)
        with open(f'data/{guild.id}/economy.json', 'r') as file:
            users = json.load(file)
            for user in users['user']:
                if str(user['id']) == _user_id:
                    usercoins = user['coins']
                    if usercoins > bet:
                        await channel.send(f'Please place a bet that is lower than your current balance. \n Your Balance: {usercoins}')


        # First Deal to User
        userc1 = random.choice(self.suits) + random.choice(self.cards)
        userc2 = random.choice(self.suits) + random.choice(self.cards)
        
        embed = discord.Embed(title='Black Jack')
        embed.add_field(name='Your Cards',
                        value=f'{userc1} , {userc2}',
                        inline=False)

        embed.add_field(name='_',
                        value='hit or stay?',
                        inline=False)

        await channel.send(embed= embed)

        #Dealer Play
        dealerc1 = random.choice(self.suits) + random.choice(self.cards)
        dealerc2 = random.choice(self.suits) + random.choice(self.cards)

        dealtotal = value(dealerc1, dealerc2)
        
        if dealtotal < 17:
            dealerc3 = random.choice(self.suits) + random.choice(self.cards)
            dealtotal = value(dealerc2, dealerc2, dealerc3)
            if dealtotal < 17:
                dealerc4 = random.choice(self.suits) + random.choice(self.cards)
                dealtotal =value(dealerc1, dealerc2, dealerc3, dealerc4)
                dealcards = [dealerc1, dealerc2, dealerc3, dealerc4]
            elif dealtotal > 17:
                dealcards = [dealerc2, dealerc2, dealerc3]
        elif dealtotal >= 17:
            dealcards = [dealerc1, dealerc2]


        #First user Choice

        def check(msg):
            return msg.author.id == _user_id and msg.channel == channel and msg.content.lower() in ['hit','stay']

        try:
            choice = await self.bot.wait_for('message',check=check, timeout= 60.0)
        
        except TimeoutError:
            await channel.send('Command Timed Out')
        
        else:


            if choice.content.lower() == 'hit':
                userc3 = random.choice(self.suits) + random.choice(self.cards)
                total = value(userc1, userc2, userc3)
                if total > 21:
                    embed.set_field_at(index=0,
                                       name='Your Cards',
                                       value=f'{userc1} , {userc2} , {userc3}',
                                       inline=False)
                    embed.insert_field_at(index=0,
                                       name='Bust!',
                                       value=f'Your total is {total}',
                                       inline=False)
                    await channel.send(embed=embed)



                else:
                    embed.set_field_at(index=0,
                                       name='Your Cards',
                                       value=f'{userc1} , {userc2} , {userc3}',
                                       inline=False)
                    await channel.send(embed=embed)


#_______    _______________________________________________________________
#   
                    # User Second Responce
                    try:
                        choice2 =  await self.bot.wait_for('message',check=check)
                    
                    except TimeoutError:
                        await channel.send('Command Timed Out')
        
                    else:
                        if choice2.content.lower() == 'hit':
                            userc4 = random.choice(self.suits) + random.choice(self.cards)
                            total = value(userc1, userc2, userc3, userc4)
                            if total > 21:
                                embed.set_field_at(index=0,
                                                   name='Your Cards',
                                                   value=f'{userc1} , {userc2} , {userc3} , {userc4}',
                                                   inline=False)
                                embed.insert_field_at(index=0,
                                                   name='Bust!',
                                                   value=f'Your total is {total}',
                                                   inline=False)
                                await channel.send(embed=embed)



                            else:
                                embed.set_field_at(index=0,
                                                   name='Your Cards',
                                                   value=f'{userc1} , {userc2} , {userc3}, {userc4}',
                                                   inline=False)
                                await channel.send(embed=embed)
            #user choice 3
                                try:
                                    choice3 =  await self.bot.wait_for('message',check=check)
                                except TimeoutError:
                                    await channel.send('Command Timed Out')
        
                                else:

                                    if choice3.content.lower() == 'hit':
                                        userc5 = random.choice(self.suits) + random.choice(self.cards)
                                        total = value(userc1, userc2, userc3, userc4)
                                        if total > 21:
                                            embed.set_field_at(index=0,
                                                               name='Your Cards',
                                                               value=f'{userc1} , {userc2} , {userc3} , {userc4} , {userc5}',
                                                               inline=False)
                                            embed.insert_field_at(index=0,
                                                               name='Bust!',
                                                               value=f'Your total is {total}',
                                                               inline=False)
                                            await channel.send(embed=embed)



                                        else:
                                            embed.set_field_at(index=0,
                                                               name='Your Cards',
                                                               value=f'{userc1} , {userc2} , {userc3} , {userc4} , {userc5}',
                                                               inline=False)
                                            embed.remove_field(1)
                                            usertotal = value(userc1,userc2,userc3,userc4,userc5)
                                            dealcardlen = len(dealcards)

                                            if dealcardlen == 2:
                                                embed.add_field(name='Dealer Cards',
                                                            value=f'{dealerc1} , {dealerc2}',
                                                            inline=False   
                                                            )
                                            elif dealcardlen == 3:
                                                embed.add_field(name='Dealer Cards',
                                                            value=f'{dealerc1} , {dealerc2} . {dealerc2}' ,  
                                                            inline=False
                                                            )
                                            elif dealcardlen == 4:
                                                embed.add_field(name='Dealer Cards',
                                                            value=f'{dealerc1} , {dealerc2} , {dealerc3} , {dealerc4}' ,
                                                            inline=False 
                                                            )
                                            else:
                                                print('Dealer card else')

                                            if usertotal > dealtotal:
                                                bet = bet + bet
                                                embed.insert_field_at(  index=1,
                                                                name='You win!',
                                                                value=f'Your bet back Plus 1x',
                                                                inline=False
                                                                )

                                            elif usertotal == dealtotal:
                                            
                                                embed.insert_field_at(  index=1,
                                                                        name='Push',
                                                                        value=f'You get your bet back',
                                                                        inline=False
                                                                        )


                                            elif dealtotal > usertotal:
                                                embed.insert_field_at(  index=1,
                                                                        name='Dealer Wins!',
                                                                        value=f'You loose your money',
                                                                        inline=False
                                                                        )



                                            await channel.send(embed=embed)


                                    elif choice3.content.lower() == 'stay':
                                        usertotal = value(userc1,userc2,userc3,userc4)
                                        embed.remove_field(1)
                                        dealcardlen = len(dealcards)

                                        if dealcardlen == 2:
                                            embed.add_field(name='Dealer Cards',
                                                        value=f'{dealerc1} , {dealerc2}' ,
                                                        inline=False  
                                                        )
                                        elif dealcardlen == 3:
                                            embed.add_field(name='Dealer Cards',
                                                        value=f'{dealerc1} , {dealerc2} , {dealerc2}' ,
                                                        inline=False  
                                                        )
                                        elif dealcardlen == 4:
                                            embed.add_field(name='Dealer Cards',
                                                        value=f'{dealerc1} , {dealerc2} , {dealerc3} , {dealerc4}' ,
                                                        inline=False  
                                                        )
                                        else:
                                            print('Dealer card else')


                                        if usertotal > dealtotal:
                                            bet = bet + bet
                                            embed.insert_field_at(  index=1,
                                                            name='You win!',
                                                            value=f'Your bet back Plus 1x',
                                                            inline=False
                                                            )

                                        elif usertotal == dealtotal:
                                        
                                            embed.insert_field_at(  index=1,
                                                                    name='Push',
                                                                    value=f'You get your bet back',
                                                                    inline=False
                                                                    )


                                        elif dealtotal > usertotal:
                                            embed.insert_field_at(  index=1,
                                                                    name='Dealer Wins!',
                                                                    value=f'You loose your money',
                                                                    inline=False
                                                                    )

                                        await channel.send(embed=embed)

                        #User Stay
                        elif choice2.content.lower() == 'stay':
                            usertotal = value(userc1,userc2,userc3)
                            embed.remove_field(1)
                            dealcardlen = len(dealcards)

                            if dealcardlen == 2:
                                embed.add_field(name='Dealer Cards',
                                            value=f'{dealerc1} , {dealerc2}',
                                            inline=False   
                                            )
                            elif dealcardlen == 3:
                                embed.add_field(name='Dealer Cards',
                                            value=f'{dealerc1} , {dealerc2} , {dealerc2}',
                                            inline=False    
                                            )
                            elif dealcardlen == 4:
                                embed.add_field(name='Dealer Cards',
                                            value=f'{dealerc1} , {dealerc2} , {dealerc3} , {dealerc4}' ,
                                            inline=False   
                                            )
                            else:
                                print('Dealer card else')



                            if usertotal > dealtotal:
                                bet = bet + bet
                                embed.add_field(
                                                name='You win!',
                                                value=f'Your bet back Plus 1x',
                                                inline=False)
                                

                            elif usertotal == dealtotal:

                                embed.insert_field_at(  index=1,
                                                        name='Push',
                                                        value=f'You get your bet back',
                                                        inline=False
                                                        )


                            elif dealtotal > usertotal:
                                embed.insert_field_at(  index=1,
                                                        name='Dealer Wins!',
                                                        value=f'You loose your money',
                                                        inline=False)

                            await channel.send(embed=embed)


#_______    ________________________________________________________________


            elif choice.content.lower() == 'stay':
                usertotal = value(userc1, userc2)
                embed.remove_field(1)
                dealcardlen = len(dealcards)
                if dealcardlen == 2:
                    embed.add_field(name='Dealer Cards',
                                value=f'{dealerc1} , {dealerc2}' ,
                                inline=False   
                                )
                elif dealcardlen == 3:
                    embed.add_field(name='Dealer Cards',
                                value=f'{dealerc1} , {dealerc2} , {dealerc2}',
                                inline=False    
                                )
                elif dealcardlen == 4:
                    embed.add_field(name='Dealer Cards',
                                value=f'{dealerc1} , {dealerc2} , {dealerc3} , {dealerc4}'  ,
                                inline=False  
                                )
                else:
                    print('Dealer card else')


                #if userc1 == userc2 and usertotal > dealtotal:
                #    #perfect pair win odds 30/1
                #    bet = bet + (bet * 30)
                #    embed.insert_field_at(  index=1,
                #                            name='',
                #                            value=f'')
#
                #elif usertotal == 21 and dealtotal < usertotal:
                #    bet = bet + (bet * 1.5)
                #    embed.insert_field_at(  index=1,
                #                            name='',
                #                            value=f'')

                if usertotal > dealtotal:
                    bet = bet + bet
                    embed.insert_field_at(  index=1,
                                            name='You win!',
                                            value=f'Your bet back Plus 1x',
                                            inline=False
                                            )

                elif usertotal == dealtotal:
                    embed.insert_field_at(  index=1,
                                            name='Push',
                                            value=f'You get your bet back',
                                            inline=False
                                            )


                elif dealtotal > usertotal:
                    embed.insert_field_at(  index=1,
                                            name='Dealer Wins!',
                                            value=f'You loose your bet',
                                            inline=False
                                            )
                
                await channel.send(embed=embed)



        

    def roulett():
        pass



def setup(bot):
    bot.add_cog(Economy(bot))