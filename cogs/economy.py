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
    async def wallet(self, ctx, *username):

        user = ctx.author
        channel = ctx.channel
        guild = ctx.guild
        if username == ():
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
        elif len(username) > 1:
            await channel.send('Please enter one name')

        else:
            #Find user and print wallet
            with open(f'data/{guild.id}/economy.json', 'r') as file:
                file.seek(0)
                users = json.load(file)
                counter = 0
                for u in users['user']:
                    if u['name'].lower() == username[0].lower():
                        coins = u['coins']
                        uname = u['name']
                        lastwork = time.localtime(int(u['lastwork']))
                        await channel.send(f'{uname} has {coins} coins and last worked on {time.asctime(lastwork)}')

                        print('user found')
                    elif counter == len(users):
                        await channel.send('User not found.')  
                file.seek(0)     
    
    
    def value(self, cards:list):
        total = 0
        counter = 1
        for card in cards:
            suit = card[0]
            nmb = card[1:]
            if nmb in ['J','Q','K']:
                total += 10
            
            elif nmb == 'A':
                if counter > 2 and total <= 10 and len(cards) == 2:
                    total += 11
                
                elif counter == 1 and len(cards) == 2:
                    total+=  11
                    
                else:
                    total += 1
            
            elif nmb in [str(x) for x in range(2,11)]:
                total += int(nmb)
            counter += 1
        
        return int(total)

    def valid_bet(self, ctx, bet):
        guild = ctx.guild
        user = ctx.author
        with open(f'data/{guild.id}/economy.json', 'r') as f:
            users = json.load(f)
            for u in users['user']:
                if str(u['id']) == str(user.id):
                    usercoins = u['coins']

                    if int(bet) < 0:
                        return False, usercoins
                        
                    elif int(usercoins) > int(bet):
                        return True, usercoins

                    else:
                        return False, usercoins


    def deal(self, hand:list):
        hand.append(random.choice(self.suits) + random.choice(self.cards))
        hand.append(random.choice(self.suits) + random.choice(self.cards))
        return hand

    def hit(self, hand:list):
        hand.append(random.choice(self.suits) + random.choice(self.cards))
        return hand

    def build_embed(self, dealer:list, hand:list, choice, bet):
        total = self.value(hand)
        embed = discord.Embed(title='Black Jack')
        embed.add_field(name ='Your Cards',
                        value=f'______',
                        inline=False)
        for card in hand:
            embed.add_field(name=f'{card}',
                        value='__',
                        inline=True)
        

        
        if choice == 'stay':
            if self.check_win(dealer, hand) == 'win':
                embed.add_field(name='YOU WIN!',
                                value=f'{bet}',
                                inline=False)
                    
            elif self.check_win(dealer, hand) == 'push':
                embed.add_field(name='PUSH!',
                                value=f'{bet}',
                                inline=False)

            elif self.check_win(dealer, hand) == 'lose':
                embed.add_field(name='YOU LOSE!',
                                value=f'{bet}',
                                inline=False)

            embed.add_field(name='Dealer Cards',
                            value=f'________',
                            inline=False)
            
            for card in dealer:
                embed.add_field(name=f'{card}',
                                value='__',
                                inline=True)  

        
        elif choice == 'hit':
            if total > 21:
                embed.add_field(name='Bust!',
                                value=f'Your total is {total}. \n{bet} ',
                                inline=False)
                
                embed.add_field(name='Dealer Cards',
                                value=f'________',
                                inline=False)
                
                for card in dealer:
                    embed.add_field(name=f'{card}',
                                    value='__',
                                    inline=True)  
            else:         
           
                embed.add_field(name ='____________',
                                value='hit or stay?',
                                inline=False)

                embed.add_field(name='Your Bet',
                                value=f'{bet}',
                                inline=False)

        return embed

    def check_win(self, dealer,  player):
        playerTotal = self.value(player)
        dealerTotal = self.value(dealer)
        if dealerTotal > 21:
            return 'win'
        
        elif playerTotal > 21:
            return 'lose'
        
        elif playerTotal > dealerTotal:
            return 'win'
        
        elif playerTotal == dealerTotal:
            return 'push'
        
        elif  playerTotal < dealerTotal:
            return 'lose'

    
    
    def settle_bet(self, ctx, bet, score):
        with open(f'data/{ctx.guild.id}/economy.json', 'r') as f:
            f.seek(0)
            users = json.load(f)
            for  u in users['user']:
                if str(ctx.author.id) == u['id']:
                    if score == 'win':
                        bet += bet
                        with open(f'data/{ctx.guild.id}/economy.json', 'w') as file:
                            u['coins'] = int(u['coins']) + bet
                            json.dump(users,file,indent=5)
                            f.seek(0)
                            file.seek(0)
                            return f'{bet} has been added to your account. \nYour new balance is {u["coins"]}'


                    elif score == 'push':
                        return f'{bet} has been returned to your account'
                        

                    elif score == 'lose':
                        with open(f'data/{ctx.guild.id}/economy.json', 'w') as file:
                            
                            u['coins'] = int(u['coins']) - bet
                            json.dump(users,file,indent=5)
                            f.seek(0)
                            file.seek(0)
                            return f'{bet} has been removed from your account. \nYour new balance is {u["coins"]}'





    @commands.command()
    async def blackjack(self, ctx, arg:int):
        guild   = ctx.guild
        channel = ctx.channel
        _user_id = ctx.author.id
        bet = arg

        valid     = self.valid_bet(ctx,arg)[0]
        usercoins = self.valid_bet(ctx,arg)[1]

        if  not valid:
            await channel.send(f'Please place a valid bet. \nYour Balance: {usercoins}')
        
        elif valid:
            userhand   = self.deal([])
            dealerhand = self.deal([])

            while self.value(dealerhand) < 17:
                dealerhand = self.hit(dealerhand)

            embed = self.build_embed(dealerhand, userhand, 'hit', bet)
        
            await channel.send(embed=embed)

            def check(msg):
                return msg.author.id == _user_id and msg.channel == channel and msg.content.lower() in ['hit','stay']

            hit = True
            while hit:

                try:
                    choice = await self.bot.wait_for('message', check=check, timeout = 60.00)
                    if choice.content.lower() == 'stay':
                        score = self.check_win(dealerhand, userhand)
                        bet = self.settle_bet(ctx, bet, score)
                        embed = self.build_embed(dealerhand, userhand, 'stay', bet)
                        hit = False
                        await channel.send(embed=embed)

                    elif choice.content.lower() == 'hit':
                        userhand = self.hit(userhand)
                        if self.value(userhand) > 21:
                            hit = False
                            bet = self.settle_bet(ctx, bet, 'lose')
                        embed = self.build_embed(dealerhand, userhand, 'hit', bet)
                        await channel.send(embed=embed)


                except TimeoutError:
                    await channel.send('Command Timed Out')



        

    def roulett():
        pass



def setup(bot):
    bot.add_cog(Economy(bot))