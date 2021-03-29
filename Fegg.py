#-------------------------------import----------------------------------#
import discord, logging, random#, asyncio
#-----------------------------------------------------------------------#

#-------------------------------variables-------------------------------#
TOKEN = '' #Bot token
PLAYERHP = 100 #Starting health for both players
#-----------------------------------------------------------------------#

#Logging errors
logging.basicConfig(level=logging.ERROR)
#logging.basicConfig(level=logging.CRITICAL)
#logging.basicConfig(level=logging.WARNING) #Errors and stuff show in the terminal

class MyClient(discord.Client):
    #-------------------------------"Global" Variables:-------------------------------#
    #Lucky numbers of the members in the Arena, as a dictionary
    luckies = {822474721525628979: 1, 259716396198395904: 2, 543857545278783520: 3, 400514653957914635: 4, 246080207704817664: 5, 567819726013726722: 6, 332711880831270912: 7, 320559692269223938: 8, 194310041900154880: 9, 548617575282769922: 10, 640714673045504020: 11, 175824478423482368: 13, 294736827946893313: 16, 748751242003611739: 18, 731368690364186634: 19}
    fighting = False #for the Arena game
    mode = ""
    MELUMI = 640714673045504020 #my discord id
    #----------------------------------------------------------------------------------#
    #Launch text in terminal
    async def on_ready(self): #login text, init fighters, self.turn = self.p1
        print(f'We have logged in as {self.user}')
        #Initialize players
        self.p1 = Fighter()
        self.p2 = Fighter()
        self.turn = self.p1

    #Reading messages
    async def on_message(self, message):
        """if message.author == client.user: #so that the bot doesn't message itself
            reself.turn
        """
        if self.fighting: #If people are self.fighting then we call fight
            await self.fight(message)
        
        message_lower = message.content.lower() #converts message to lowercase (cuz it's used a lot)
        if message_lower.startswith('!'): 
            if message_lower.startswith("!fight"): #begin fight if no one is self.fighting
                if not self.fighting:
                    await self.startfight(message)
                else: 
                    await message.channel.send(f"There is already a fight going on between {self.p1.tag} and {self.p2.tag} and the maker of this bot did not anticipate that he needed to add code for more than one battle at a time. Please contact self.MELUMI#5395 or ask the current fighters to wrap up or quit their game. Thank you.")

            elif message_lower == '!sweat': #big sweat
                await message.channel.send("https://cdn.discordapp.com/attachments/822493563619246131/822498710873178133/unknown.png")

            elif message_lower == '!forceresume': #resumes fight if accidentally quit
                if message.author.id in {self.p1.id, self.p2.id, self.MELUMI}:
                    self.fighting = True
                    await self.reporthp(message, "FORCERESUME")
            
            elif message_lower.startswith("!roll d"): #dice roll command (up to 999)
                try:
                    await message.channel.send(str(random.randint(1, int(message.content[7:]))))
                except: pass
            
            elif message_lower == '!help': #help command
                embedVar = discord.Embed(title="Hello", description="My name is Fegg. I am a bot coded by self.MELUMI#5395", color=0x00ff00)
                embedVar.add_field(name=("List of commands:"), value="!help (this command)\n!fight (fight command for the Arena)\n!sweat (:colinsweat:)\n!roll (rolls a die, syntax: `!roll d20`)", inline=False)
                await message.channel.send(embed=embedVar)
            
            elif message_lower.startswith("!setlucky"):
                if message.author.id in self.luckies.keys():
                    await message.channel.send("Your lucky number is already set as " + str(self.luckies[message.author.id]))
                elif len(message.content) <= 10:
                    await message.channel.send("Please type the command like `!setlucky 1` or `!setlucky 11`")
                else: 
                    if message.content[10:].isdigit():
                        num = message.content[10:]
                        if 0 < num <= 20:
                            self.luckies[message.author.id] = num
                            await message.channel.send("Your lucky number has been temporarily set as " + str(self.luckies[message.author.id]))
                        else: await message.channel.send("Please use a number between 1 and 20 such as `!setlucky 11`")

        elif 'kill me' in message_lower or ('i ' in message_lower and 'die' in message_lower): #suicide prevention
            await message.channel.send("Please not worry. @everyone is here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/")
            await message.author.send('Please do not worry. We are here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/')

        elif 'parm' in message_lower: #parm
            await message.channel.send("https://images.heb.com/is/image/HEBGrocery/000081264")

    async def startfight(self, message): #called when a fight starts
        #self.fighting is still false
        self.turn = self.p1
        self.p1.reset(message.author)#initiates player 1 with PLAYERHP
        try:
            self.p2.reset(message.mentions[0]) #inits player 2 the same way
        except IndexError:
            await message.channel.send("Please use `!fight @someone` if you want to fight them.") #if there is no mention, give error
        else: #self.fighting is still False
            if self.p1.id == self.p2.id:
                await message.channel.send("You can't fight yourself.") #you can't fight yourself, and this also triggers if no mention
                self.fighting = False
            else: #try self.luckies, start fight
                self.fighting = True
                self.mode = ""
                try: #checks if the lucky numbers are registered
                    embedVar = discord.Embed(title=(f"**{self.p1.tag.name}** challenges **{self.p2.tag.name}** to a battle!"), description="The first player to lose all their health loses.", color=0x00ff00)
                    embedVar.add_field(name=(f"**{self.p1.tag.name}**'s lucky number is {self.luckies[self.p1.id]} and **{self.p2.tag.name}**'s is {self.luckies[self.p2.id]}."), 
                                        value=("Type `roll` to attack and `!quit` to stop self.fighting."), inline=False)
                    embedVar.set_thumbnail(url=(message.author.avatar_url))
                    await message.channel.send(embed=embedVar)
                except KeyError: #checks whose lucky number isn't registered
                    try:
                        self.luckies[self.p1.id] #checking to see both players' lucky numbers are registered
                    except KeyError:
                        await message.channel.send(f"Uh oh, {self.p1.name}'s lucky number is not in my database. Please ask {self.MELUMI} for help.")
                        self.fighting = False
                    try:
                        self.luckies[self.p2.id]
                    except KeyError:
                        await message.channel.send(f"Uh oh, {self.p2.name}'s lucky number is not in my database. Please ask {self.MELUMI} for help.\nYou can also use `!setlucky` to temporarily set your lucky number to fight.")
                        self.fighting = False

    async def fight(self, message): #called everytime fight is active, processes rolls.
        if self.mode == "17": #if the last roll was a 17
            if 'attack' in message.content.lower(): #attacks for 17
                if message.author.id == self.turn.id:
                    self.damage = 17
                    if self.turn.id == self.p1.id: self.other = self.p2 #Regular attacking biz
                    else: self.other = self.p1
                    self.other.hp -= self.damage
                    await self.reporthp(message, str(self.damage)) #The order in which these occur matters.
                    self.turn = self.other
                    await self.checkstuff(message, self.damage)
                    self.mode = ""
                else: await message.channel.send("Who are you?")
            if 'heal' in message.content.lower(): #heals for 4d7
                if message.author.id == self.turn.id:
                    self.damage = random.randint(1, 7) + random.randint(1, 7) + random.randint(1, 7) + random.randint(1, 7)
                    self.turn.seventeens += 1 #update stats
                    self.turn.hp += self.damage #heal
                    if self.turn.id == self.p1.id: self.other = self.p2
                    else: self.other = self.p1
                    #Instead of self.reporthp
                    embedVar = discord.Embed(title=(f"{self.turn.tag.name} healed **{self.damage}** health!"), description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"), color=0x00ff00)
                    embedVar.set_author(name=self.turn.tag.name, icon_url=(self.turn.tag.avatar_url))
                    await message.channel.send(embed=embedVar)
                    self.mode = ""
                    self.turn = self.other
                    #await self.checkstuff(message, self.damage) #we shouldn't need this
                else: await message.channel.send("Who are you?")
        if message.content.lower() == "roll":
            if self.mode == "17": #if the last roll was 17 then don't roll
                await message.channel.send("Please choose whether to `heal` or `attack`.")
            elif self.mode == "clash": #keep clashing
                await self.clash(message)
            elif message.author.id == self.turn.id: #the person whose self.turn it is rolls
                if self.turn.id == self.p1.id and self.p2.hp - self.p1.hp >= 30: self.damage = random.randint(1, 30)
                elif self.turn.id == self.p2.id and self.p1.hp - self.p2.hp >= 30: self.damage = random.randint(1, 30)
                else: self.damage = random.randint(1, 20)
                if self.turn == self.p1: 
                    self.p1.last = self.damage
                    self.p1.rolls.append(self.damage)
                    self.other = self.p2
                else: 
                    self.other = self.p1
                    if self.p1.last == self.damage: #if self.p1's last is self.p2's current
                        self.mode = "clash"
                        await self.clashstart(message, self.damage) #doesn't self.reporthp, quits this function
                        return
                await self.processattack(message, self.damage)
                if self.mode == "17": #not sure if this is needed
                    return
                self.other.hp -= self.damage
                await self.reporthp(message, str(self.damage)) #The order in which these occur matters.
                await self.checkstuff(message, self.damage) #checks if game is over
                self.turn = self.other
                await message.channel.send("roll") #fegg attack, will remove later

        if message.content.lower() == "!quit" and (message.author.id == self.p1.id or message.author.id == self.p2.id): #to abort the match
            embedVar = discord.Embed(title=f"The match between {self.p1.tag.name} and {self.p2.tag.name} has been aborted.", description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"), color=0x00ff00)
            embedVar.add_field(name="Have a nice day!", value="||(if this was an accident, please try !forceresume)||", inline=False)
            await message.channel.send(embed=embedVar) #match over and hp text
            await self.reportstats(message)
            self.fighting = False #stops the fight
            self.mode = ""

    #called when game ends
    async def reportstats(self, message):
        embedVar = discord.Embed(title=(self.p1.tag.name + "'s stats:"), description=self.p1.stats(), color=0x00ff00)
        embedVar.set_thumbnail(url=(self.p1.tag.avatar_url)) #stats for player 1
        await message.channel.send(embed=embedVar)

        embedVar = discord.Embed(title=(self.p2.tag.name + "'s stats:"), description=self.p2.stats(), color=0x00ff00)
        embedVar.set_thumbnail(url=(self.p2.tag.avatar_url)) #stats for player 2
        await message.channel.send(embed=embedVar)

    #runs after someone rolls
    async def processattack(self, message, dmg):
        if dmg == 1: #self.damage = 0, updates stats
            embedVar = discord.Embed(title=("You got a one!!"), description="You miss your attack. *oof*", color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.turn.ones += 1
            self.damage = 0
        elif dmg == self.luckies[self.turn.id]: #heals 10HP, updates stats
            embedVar = discord.Embed(title=("You got your lucky number!"), description="You heal 10HP.", color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.turn.hp += 10
            self.turn.luckies += 1
            self.damage = self.luckies[self.turn.id]
        elif dmg == 17: #sets self.mode to 17, self.damage 0
            embedVar = discord.Embed(title=("You got a 17!"), description="Would you like to `heal` or `attack`?\n(Attacking does 17 damage and healing rolls a 4d7.\nStats are only updated if you choose to heal.", color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.mode = "17"
            self.damage = 0
        elif dmg == 20: #updates stats
            embedVar = discord.Embed(title=("You got a 20!"), description="||It doesn't do anything special, but your stats will be updated :pray:||", color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.turn.twenties += 1
            self.damage = 20
        elif dmg == 30: #special message
            embedVar = discord.Embed(title=("You got a 30!"), description="If you don't already have the award, please take care of that as I don't track awards.", color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.damage = 30

    #runs after processattack, after someone rolls
    async def reporthp(self, message, damage):
        embedVar = discord.Embed(title=(f"{self.turn.tag.name} did **{damage}** damage!"), description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"), color=0x00ff00)
        embedVar.set_author(name=(self.turn.tag.name + " roll"), icon_url=(self.turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)

    #Checks if the game is over, including draw clash
    async def checkstuff(self, message):
        if self.turn == self.p2:
            if self.p1.hp <= 0 and self.p2.hp <= 0: #draw
                embedVar = discord.Embed(title=f"The match between {self.p1.tag.name} and {self.p2.tag.name} has ended in a draw.", description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"), color=0x00ff00)
                embedVar.add_field(name=("Please update your stats with a draw."), value="If you would like to draw clash for the award, you can use `!roll d100` and win 3 out of 5 rolls.", inline=False)
                await message.channel.send(embed=embedVar) #match over and hp text
                await self.reportstats(message)
                self.fighting = False #stops the fight
                self.mode = ""
            elif self.p1.hp <= 0 or self.p2.hp <= 0:
                embedVar = discord.Embed(title=f"The match between {self.p1.tag.name} and {self.p2.tag.name} has ended.", description=f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}\nPlease update your stats and awards, and try to remember as I can't check all of them.", color=0x00ff00)
                await message.channel.send(embed=embedVar) #match over and hp text
                await self.reportstats(message)
                self.fighting = False
                self.mode = ""
                if self.p1.hp == 0 or self.p2.hp == 0:
                    embedVar = discord.Embed(title=("You finished your opponent with the exact number!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp <= -15 or self.p2.hp <= -15:
                    embedVar = discord.Embed(title=("You finished your opponent to -15 HP!"), description="You may be eligible for an award if you don't already have it.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp >= 30 or self.p2.hp >= 30:
                    embedVar = discord.Embed(title=("You finished your opponent with 30 health left!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp >= 50 or self.p2.hp >= 50:
                    embedVar = discord.Embed(title=("You finished your opponent with 50 health left!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp >= 70 or self.p2.hp >= 70:
                    embedVar = discord.Embed(title=("You finished your opponent with 70 health left!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if (self.p1.rolls[0] == 20 and self.p2.rolls[0] == 1) or (self.p2.rolls[0] == 20 and self.p2.rolls[0] == 1):
                    embedVar = discord.Embed(title=("Your first roll was a 20 and your opponent's was a miss!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if (self.p1.rolls[-1] == self.luckies[self.p1.id]) or (self.p2.rolls[-1] == self.luckies[self.p2.id]):
                    embedVar = discord.Embed(title=("You finished your opponent with your lucky number!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if (self.p1.rolls[-1] == 20) or (self.p2.rolls[-1] == 20):
                    embedVar = discord.Embed(title=("You finished your opponent with a special attack!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
        for i in {self.p1, self.p2}: #3 in a row
            if i.rolls[-1] == i.rolls[-2] and i.rolls[-2] == i.rolls[-3]:
                embedVar = discord.Embed(title=("You got three in a row!"), description="You get a bonus attack! You can also claim an award if you don't already have it :D", color=0x00ff00)
                embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
                await message.channel.send(embed=embedVar)
                self.turn = i
        if (self.p1.hp >= 125) or (self.p2.hp >= 125):
                embedVar = discord.Embed(title=("You have over 125 health!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)

    #Start clash text, sets self.turn to self.p1
    async def clashstart(self, message, damage):
        embedVar = discord.Embed(title=("Clash!"), description="Both players got a " + str(damage), color=0x00ff00)
        embedVar.add_field(name="Both players will now roll d100s", value="You need to win two out of three rolls.\n" + self.p1.name + " goes first.", inline=False)
        await message.channel.send(embed=embedVar)
        self.turn = self.p1

    #Processes clash rolls
    async def clash(self, message):
        if message.content.lower() == "roll":
            if message.author.id == self.turn.id:
                self.damage = random.randint(1, 100)
                if self.damage == 1: #sets self.other person's clash score to 2 and says you lose
                    if self.turn.id == self.p1.id: self.p2.clash = 2
                    else: self.p1.clash = 2
                    await message.channel.send("You automatically lose the clash. oof.")
                if self.damage == 100: #sets clash score to 2, mentions award
                    self.turn.clash = 2
                    await message.channel.send("You automatically win the clash. If you don't already have the award, please claim it now.")
                if self.turn.id == self.p1.id:
                    self.p2.last = self.damage #for checking who won the round 
                else: #self.turn is self.p2, time to check stuff
                    if self.damage > self.p2.last:
                        self.p2.clash += 1 #checks who won the clash
                    elif self.damage < self.p2.last:
                        self.p1.clash += 1
                    else:
                        await message.channel.send("wtf you got the same number and idk what to do so I won't count this one")
                    if self.p1.clash >= 2: winner = self.p1
                    elif self.p2.clash >= 2: winner = self.p2
                    if winner.clash >= 2: #winner text and stuff, quits function
                        winner.hp += self.p1.last
                        embedVar = discord.Embed(title=(winner.tag.name + " won the clash!"), description=f"The clash score is:\n{self.p1.name}: {self.p1.clash}\n{self.p2.name}: {self.p2.clash}", color=0x00ff00)
                        embedVar.set_thumbnail(url=(winner.avatar_url))
                        await message.channel.send(embed=embedVar)
                        await self.reporthp(message, self.p1.last)
                        self.mode = ""
                        self.p2.last = -1
                        self.turn = self.p1
                        winner.clashwins += 1
                        winner = None
                        self.p1.clash, self.p2.clash = 0, 0
                        return
                embedVar = discord.Embed(title=(f"{self.turn.tag.name} got a **{self.damage}**!!"), description=(f"The clash score is:\n{self.p1.name}: {self.p1.clash}\n{self.p2.name}: {self.p2.clash}"), color=0x00ff00)
                embedVar.set_author(name=(self.turn.tag.name + " roll"), icon_url=(self.turn.tag.avatar_url))
                await message.channel.send(embed=embedVar) #Reports roll
                if self.turn.id == self.p1.id: self.turn = self.p2
                else: self.turn = self.p1

class Fighter: #Arena game player class
        def reset(self, tag):
            self.tag = tag #discord tag
            self.id = self.tag.id #the long number
            #self.name = "<@" +str(self.id) + ">" #<@numbers>
            self.name = self.tag.name
            self.hp = PLAYERHP #100 by default, set at top
            self.ones = 0
            self.twenties = 0
            self.luckies = 0
            self.seventeens = 0
            self.clashwins = 0

            self.last = -1
            self.clash = 0
            self.rolls = []

        def stats(self):
            return (f"{self.name} got **{self.ones}** ones, **{self.twenties}** twenties,\n**{self.luckies}** lucky numbers, **{self.seventeens}** seventeens, and **{self.clashwins}** clash wins.")

client = MyClient()
#Launch bot
with open('token.txt') as f:
    TOKEN = f.readline()
client.run(TOKEN)

#Reference

#wait:
#await asyncio.sleep(10)
#reply:
#await message.channel.reply('Hello!', mention_author=False)