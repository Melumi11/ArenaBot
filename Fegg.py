#-------------------------------import----------------------------------#
import discord, logging, asyncio, random
#-----------------------------------------------------------------------#

#-------------------------------variables-------------------------------#
client = discord.Client()
TOKEN = '' #Bot token
#Lucky numbers of the members in the Arena, as a dictionary
luckies = {822474721525628979: 1, 259716396198395904: 2, 543857545278783520: 3, 400514653957914635: 4, 246080207704817664: 5, 567819726013726722: 6, 332711880831270912: 7, 320559692269223938: 8, 194310041900154880: 9, 548617575282769922: 10, 640714673045504020: 11, 175824478423482368: 13, 294736827946893313: 16, 748751242003611739: 18, 731368690364186634: 19}
fighting = False #for the Arena game
#p1, p2 = None, None #defining players, will be changed to Fighter class on init
PLAYERHP = 100 #Starting health for both players
mode = ""
MELUMI = 640714673045504020
#-----------------------------------------------------------------------#

#Logging errors
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)
logging.basicConfig(level=logging.WARNING) #Errors and stuff show in the terminal

#Launch text in terminal
@client.event
async def on_ready(): #login text, init fighters, turn = p1
    print('We have logged in as {0.user}'.format(client))
    #Initialize players
    global p1
    global p2
    global turn
    p1 = Fighter()
    p2 = Fighter()
    turn = p1

#Reading messages
@client.event
async def on_message(message):
    """if message.author == client.user: #so that the bot doesn't message itself
        return
    """
    global fighting #takes fighting status variable
    if fighting == True: #If people are fighting then we call fight
        await asyncio.gather(fight(message))
    
    lower = message.content.lower() #converts message to lowercase (cuz it's used a lot)
    if message.content.startswith('!'): 
        if message.content.startswith("!fight"): #begin fight if no one is fighting
            if fighting == False:
                await asyncio.gather(startfight(message))
            else: 
                await message.channel.send("There is already a fight going on between " + str(p1.tag) + " and " + str(p2.tag) + " and the maker of this bot did not anticipate that he needed to add code for more than one battle at a time. Please contact Melumi#5395 or ask the current fighters to wrap up or quit their game. Thank you.")

        elif lower == '!sweat': #big sweat
            await message.channel.send("https://cdn.discordapp.com/attachments/822493563619246131/822498710873178133/unknown.png")

        elif (lower == '!forceresume'): #resumes fight if accidentally quit
         if (message.author.id == p1.id or message.author.id == p2.id or message.author.id == MELUMI):
            fighting = True
            await asyncio.gather(reporthp(message, "FORCERESUME"))
        
        elif message.content.startswith("!roll d"): #dice roll command (up to 999)
            try:
                if len(message.content) == 8: await message.channel.send(str(random.randint(1, int(message.content[7]))))
                if len(message.content) == 9: await message.channel.send(str(random.randint(1, (int(message.content[7]) * 10 + int(message.content[8])))))
                if len(message.content) == 10: await message.channel.send(str(random.randint(1, (int(message.content[7]) * 100 + int(message.content[8]) * 10) + int(message.content[9]))))
            except: pass
        
        elif (lower == '!help'): #help command
            embedVar = discord.Embed(title="Hello", description="My name is Fegg. I am a bot coded by Melumi#5395", color=0x00ff00)
            embedVar.add_field(name=("List of commands:"), value="!help (this command)\n!fight (fight command for the Arena)\n!sweat (:colinsweat:)\n!roll (rolls a die, syntax: `!roll d20`)", inline=False)
            await message.channel.send(embed=embedVar)
        
    elif ('kill me' or ('i ' and 'die')) in lower: #suicide prevention
        await message.channel.send("Please not worry. @everyone is here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/")
        await message.author.send('Please do not worry. We are here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/')

    elif 'parm' in lower: #parm
        await message.channel.send("https://images.heb.com/is/image/HEBGrocery/000081264")
    

async def startfight(message): #called when a fight starts
    global turn
    global fighting
    global p1 #gets player variables
    global p2 #fighting = False
    turn = p1
    p1.reset(message.author)#initiates player 1 with PLAYERHP
    try:
        p2.reset(message.mentions[0]) #inits player 2 the same way
    except IndexError:
        await message.channel.send("Please use `!fight @someone` if you want to fight them.") #if there is no mention, give error
    else: #Fighting is still False
        if p1.id == p2.id:
            await message.channel.send("You can't fight yourself.") #you can't fight yourself, and this also triggers if no mention
            fighting = False
        else: #try luckies, start fight
            fighting = True
            global mode
            mode = ""
            try: #checks if the lucky numbers are registered
                embedVar = discord.Embed(title=("**" + p1.tag.name + "** challenges **" + p2.tag.name + "** to a battle!"), description="The first player to lose all their health loses.", color=0x00ff00)
                embedVar.add_field(name=("**" + p1.tag.name + "**'s lucky number is " + str(luckies[p1.id]) + " and **" + p2.tag.name + "**'s is " + str(luckies[p2.id])), 
                                    value=("Type `roll` to attack and `!quit` to stop fighting."), inline=False)
                embedVar.set_thumbnail(url=(message.author.avatar_url))
                await message.channel.send(embed=embedVar)
            except KeyError: #checks whose lucky number isn't registered
                try:
                    luckies[p1.id] #checking to see both players' lucky numbers are registered
                except KeyError:
                    await message.channel.send("Uh oh, " + p1.name + "'s lucky number is not in my database. Please ask <@640714673045504020> for help.")
                    fighting = False
                try:
                    luckies[p2.id]
                except KeyError:
                    await message.channel.send("Uh oh, " + p2.name + "'s lucky number is not in my database. Please ask <@640714673045504020> for help.")
                    fighting = False

async def fight(message): #called everytime fight is active, processes rolls.
    global p1
    global p2
    global fighting
    global turn
    global mode
    global other
    global damage
    if (mode == "17"): #if the last roll was a 17
        if ('attack' in message.content.lower()): #attacks for 17
            if (message.author.id == turn.id):
                damage = 17
                if turn.id == p1.id: other = p2 #Regular attacking biz
                else: other = p1
                other.hp -= damage
                await asyncio.gather(reporthp(message, str(damage))) #The order in which these occur matters.
                turn = other
                await asyncio.gather(checkstuff(message, damage))
                mode = ""
            else: await message.channel.send("Who are you?")
        if ('heal' in message.content.lower()): #heals for 4d7
            if (message.author.id == turn.id):
                damage = random.randint(1, 7) + random.randint(1, 7) + random.randint(1, 7) + random.randint(1, 7)
                turn.seventeens += 1 #update stats
                turn.hp += damage #heal
                if turn.id == p1.id: other = p2
                else: other = p1
                #Instead of reporthp
                embedVar = discord.Embed(title=(turn.tag.name + " healed **" + str(damage) + "** health!"), description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)), color=0x00ff00)
                embedVar.set_author(name=turn.tag.name, icon_url=(turn.tag.avatar_url))
                await message.channel.send(embed=embedVar)
                mode = ""
                turn = other
                #await asyncio.gather(checkstuff(message, damage)) #we shouldn't need this
            else: await message.channel.send("Who are you?")
    if (message.content.lower() == "roll"):
        if mode == "17": #if the last roll was 17 then don't roll
            await message.channel.send("Please choose whether to `heal` or `attack`.")
        elif mode == "clash": #keep clashing
            await asyncio.gather(clash(message))
        elif message.author.id == turn.id: #the person whose turn it is rolls
            if (turn.id == p1.id and p2.hp - p1.hp >= 30): damage = random.randint(1, 30)
            elif (turn.id == p2.id and p1.hp - p2.hp >= 30): damage = random.randint(1, 30)
            else: damage = random.randint(1, 20)
            if turn == p1: 
                p1.last = damage
                p1.rolls.append(damage)
                other = p2
            else: 
                other = p1
                if p1.last == damage: #if p1's last is p2's current
                    mode = "clash"
                    await asyncio.gather(clashstart(message, damage)) #doesn't reporthp, quits this function
                    return
            await asyncio.gather(processattack(message, damage))
            if mode == "17": #not sure if this is needed
                return
            other.hp -= damage
            await asyncio.gather(reporthp(message, str(damage))) #The order in which these occur matters.
            await asyncio.gather(checkstuff(message, damage)) #checks if game is over
            turn = other
            await message.channel.send("roll") #fegg attack, will remove later

    if (message.content.lower() == "!quit" and (message.author.id == p1.id or message.author.id == p2.id)): #to abort the match
        embedVar = discord.Embed(title="The match between " + p1.tag.name + " and " + p2.tag.name + " has been aborted.", description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)), color=0x00ff00)
        embedVar.add_field(name="Have a nice day!", value="||(if this was an accident, please try !forceresume)||", inline=False)
        await message.channel.send(embed=embedVar) #match over and hp text
        await asyncio.gather(reportstats(message))
        fighting = False #stops the fight
        mode = ""

#called when game ends
async def reportstats(message):
    global p1
    global p1
    embedVar = discord.Embed(title=(p1.tag.name + "'s stats:"), description=p1.stats(), color=0x00ff00)
    embedVar.set_thumbnail(url=(p1.tag.avatar_url)) #stats for player 1
    await message.channel.send(embed=embedVar)

    embedVar = discord.Embed(title=(p2.tag.name + "'s stats:"), description=p2.stats(), color=0x00ff00)
    embedVar.set_thumbnail(url=(p2.tag.avatar_url)) #stats for player 2
    await message.channel.send(embed=embedVar)

#runs after someone rolls
async def processattack(message, dmg):
    global turn
    global damage
    if dmg == 1: #damage = 0, updates stats
        embedVar = discord.Embed(title=("You got a one!!"), description="You miss your attack. *oof*", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        turn.ones += 1
        damage = 0
    elif dmg == luckies[turn.id]: #heals 10HP, updates stats
        embedVar = discord.Embed(title=("You got your lucky number!"), description="You heal 10HP.", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        turn.hp += 10
        turn.luckies += 1
        damage = luckies[turn.id]
    elif dmg == 17: #sets mode to 17, damage 0
        embedVar = discord.Embed(title=("You got a 17!"), description="Would you like to `heal` or `attack`?\n(Attacking does 17 damage and healing rolls a 4d7.\nStats are only updated if you choose to heal.", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        global mode
        mode = "17"
        damage = 0
    elif dmg == 20: #updates stats
        embedVar = discord.Embed(title=("You got a 20!"), description="||It doesn't do anything special, but your stats will be updated :pray:||", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        turn.twenties += 1
        damage = 20
    elif dmg == 30: #special message
        embedVar = discord.Embed(title=("You got a 30!"), description="If you don't already have the award, please take care of that as I don't track awards.", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        damage = 30

#runs after processattack, after someone rolls
async def reporthp(message, damage):
    global p1
    global p2
    global turn
    embedVar = discord.Embed(title=(turn.tag.name + " did **" + damage + "** damage!"), description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)), color=0x00ff00)
    embedVar.set_author(name=(turn.tag.name + " roll"), icon_url=(turn.tag.avatar_url))
    await message.channel.send(embed=embedVar)

#Checks if the game is over, including draw clash
async def checkstuff(message, damage):
    if turn == p2:
        global fighting
        global mode
        if (p1.hp <= 0 and p2.hp <= 0): #draw
            embedVar = discord.Embed(title="The match between " + p1.tag.name + " and " + p2.tag.name + " has ended in a draw.", description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)), color=0x00ff00)
            embedVar.add_field(name=("Please update your stats with a draw."), value="If you would like to draw clash for the award, you can use `!roll d100` and win 3 out of 5 rolls.", inline=False)
            await message.channel.send(embed=embedVar) #match over and hp text
            await asyncio.gather(reportstats(message))
            fighting = False #stops the fight
            mode = ""
        elif (p1.hp <= 0 or p2.hp <= 0):
            embedVar = discord.Embed(title="The match between " + p1.tag.name + " and " + p2.tag.name + " has ended.", description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)) + "\nPlease update your stats and awards, and try to remember as I can't check all of them.", color=0x00ff00)
            await message.channel.send(embed=embedVar) #match over and hp text
            await asyncio.gather(reportstats(message))
            fighting = False
            mode = ""
            if (p1.hp == 0 or p2.hp == 0):
                embedVar = discord.Embed(title=("You finished your opponent with the exact number!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
            if (p1.hp <= -15 or p2.hp <= -15):
                embedVar = discord.Embed(title=("You finished your opponent to -15 HP!"), description="You may be eligible for an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
            if (p1.hp >= 30 or p2.hp >= 30):
                embedVar = discord.Embed(title=("You finished your opponent with 30 health left!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
            if (p1.hp >= 50 or p2.hp >= 50):
                embedVar = discord.Embed(title=("You finished your opponent with 50 health left!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
            if (p1.hp >= 70 or p2.hp >= 70):
                embedVar = discord.Embed(title=("You finished your opponent with 70 health left!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
            if ((p1.rolls[0] == 20 and p2.rolls[0] == 1) or (p2.rolls[0] == 20 and p2.rolls[0] == 1)):
                embedVar = discord.Embed(title=("Your first roll was a 20 and your opponent's was a miss!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
            if ((p1.rolls[-1] == luckies[p1.id]) or (p2.rolls[-1] == luckies[p2.id])):
                embedVar = discord.Embed(title=("You finished your opponent with your lucky number!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
            if ((p1.rolls[-1] == 20) or (p2.rolls[-1] == 20)):
                embedVar = discord.Embed(title=("You finished your opponent with a special attack!"), description="You can get an award if you don't already have it.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
    if ((p1.hp >= 125) or (p2.hp >= 125)):
            embedVar = discord.Embed(title=("You have over 125 health!"), description="You can get an award if you don't already have it.", color=0x00ff00)
            await message.channel.send(embed=embedVar)

#Start clash text, sets turn to p1
async def clashstart(message, damage):
    global turn
    embedVar = discord.Embed(title=("Clash!"), description="Both players got a " + str(damage), color=0x00ff00)
    embedVar.add_field(name="Both players will now roll d100s", value="You need to win two out of three rolls.\n" + p1.name + " goes first.", inline=False)
    await message.channel.send(embed=embedVar)
    turn = p1

#Processes clash rolls
async def clash(message):
    if (message.content.lower() == "roll"):
        global turn
        if message.author.id == turn.id:
            damage = random.randint(1, 100)
            if damage == 1: #sets other person's clash score to 2 and says you lose
                if turn.id == p1.id: p2.clash = 2
                else: p1.clash = 2
                await message.channel.send("You automatically lose the clash. oof.")
            if damage == 100: #sets clash score to 2, mentions award
                turn.clash = 2
                await message.channel.send("You automatically win the clash. If you don't already have the award, please claim it now.")
            if turn.id == p1.id:
                p2.last = damage #for checking who won the round 
            else: #turn is p2, time to check stuff
                if damage > p2.last:
                    p2.clash += 1 #checks who won the clash
                elif damage < p2.last:
                    p1.clash += 1
                else:
                    await message.channel.send("wtf you got the same number and idk what to do so I won't count this one")
                global mode
                if p1.clash >= 2: winner = p1
                elif p2.clash >= 2: winner = p2
                if winner.clash >= 2: #winner text and stuff, quits function
                    winner.hp += p1.last
                    embedVar = discord.Embed(title=(winner.tag.name + " won the clash!"), description=("The clash score is: " + p1.name + ": " + str(p1.clash) + p2.name + ": " + str(p2.clash)), color=0x00ff00)
                    embedVar.set_thumbnail(url=(winner.avatar_url))
                    await message.channel.send(embed=embedVar)
                    await asyncio.gather(reporthp(message, p1.last))
                    mode = ""
                    p2.last = -1
                    turn = p1
                    winner.clashwins += 1
                    winner = None
                    p1.clash, p2.clash = 0, 0
                    return
            embedVar = discord.Embed(title=(turn.tag.name + " got a **" + str(damage) + "**!!"), description=("The clash score is: \n" + p1.name + ": " + str(p1.clash) + "\n" + p2.name + ": " + str(p2.clash)), color=0x00ff00)
            embedVar.set_author(name=(turn.tag.name + " roll"), icon_url=(turn.tag.avatar_url))
            await message.channel.send(embed=embedVar) #Reports roll
            if turn.id == p1.id: turn = p2
            else: turn = p1

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
        return (self.name + " got **" + str(self.ones) + "** ones, **" + str(self.twenties) + "** twenties,\n **" + str(self.luckies) + "** lucky numbers, **" + str(self.seventeens) + "** seventeens, and **" + str(self.clashwins) + "** clash wins.")

#Launch bot
with open('token.txt') as f:
    TOKEN = f.readline()
client.run(TOKEN)

#Reference

#wait:
#await asyncio.sleep(10)
#reply:
#await message.channel.reply('Hello!', mention_author=False)