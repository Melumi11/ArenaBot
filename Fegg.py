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
    
    if message.content.startswith("!fight"): #begin fight if no one is fighting
        if fighting == False:
            await asyncio.gather(startfight(message))
        else: 
            await message.channel.send("There is already a fight going on between " + str(p1.tag) + " and " + str(p2.tag) + " and the maker of this bot did not anticipate that he needed to add code for more than one battle at a time. Please contact Melumi#5395 or ask the current fighters to wrap up or quit their game. Thank you.")
        
    elif ('kill me' or ('i ' and 'die')) in message.content.lower(): #suicide prevention
        await message.channel.send("Please not worry. @everyone is here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/")
        await message.author.send('Please do not worry. We are here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/')

    elif 'parm' in message.content.lower(): #parm
        await message.channel.send("https://images.heb.com/is/image/HEBGrocery/000081264")

    elif message.content.lower() == '!sweat': #big sweat
        await message.channel.send("https://cdn.discordapp.com/attachments/822493563619246131/822498710873178133/unknown.png")
    
    elif 'fegg' in message.content.lower(): #greetings
        embedVar = discord.Embed(title="Hello", description="My name is Fegg.", color=0x00ff00)
        embedVar.add_field(name="Your name is "+ str(message.author.name), value="hi :D", inline=False)
        embedVar.set_thumbnail(url=(message.author.avatar_url))
        await message.channel.send(embed=embedVar)

    elif (message.content.lower() == '!forceresume'):
         if (message.author.id == p1.id or message.author.id == p2.id or message.author.id == MELUMI):
            fighting = True
            await asyncio.gather(reporthp(message, "FORCERESUME"))
        

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
        else:
            fighting = True
            try:
                embedVar = discord.Embed(title=("**" + p1.tag.name + "** challenges **" + p2.tag.name + "** to a battle!"), description="The first player to lose all their health loses.", color=0x00ff00)
                embedVar.add_field(name=("**" + p1.tag.name + "**'s lucky number is " + str(luckies[p1.id]) + " and **" + p2.tag.name + "**'s is " + str(luckies[p2.id])), 
                                    value=("Type `roll` to attack and `!quit` to stop fighting."), inline=False)
                embedVar.set_thumbnail(url=(message.author.avatar_url))
                await message.channel.send(embed=embedVar)
                """
                await message.channel.send(p1.name + " challenges " + p2.name + " to a battle!") #if no errors, the battle text comes
                await message.channel.send("The first person to lose all their health loses.")
                await message.channel.send("Type `roll` to attack and `!quit` to stop fighting.")
                await message.channel.send(p1.name + "'s lucky number is " + str(luckies[p1.id]) + " and " + p2.name + "'s is " + str(luckies[p2.id]))
                """
            except KeyError:
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

async def fight(message):
    global p1
    global p2
    global fighting
    global turn
    global mode
    global other
    global damage
    if (mode == "17"):
        if ('attack' in message.content.lower()):
            if (message.author.id == turn.id):
                damage = 17
                if turn.id == p1.id: other = p2
                else: other = p1
                other.hp -= damage
                await asyncio.gather(reporthp(message, str(damage))) #The order in which these occur matters.
                turn = other
                await asyncio.gather(checkstuff(message, damage))
            else: await message.channel.send("Who are you?")
        if ('heal' in message.content.lower()):
            if (message.author.id == turn.id):
                damage = random.randint(1, 7) + random.randint(1, 7) + random.randint(1, 7) + random.randint(1, 7)
                turn.seventeens += 1
                turn.hp += damage
                if turn.id == p1.id: other = p2
                else: other = p1
                #Instead of reporthp
                embedVar = discord.Embed(title=(turn.tag.name + " healed **" + damage + "** health!"), description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)), color=0x00ff00)
                embedVar.set_author(name=turn.tag.name, icon_url=(turn.tag.avatar_url))
                await message.channel.send(embed=embedVar)

                turn = other
                await asyncio.gather(checkstuff(message, damage))
            else: await message.channel.send("Who are you?")
    if (message.content.lower() == "roll"):
        if mode == "17":
            await message.channel.send("Please choose whether to `heal` or `attack`.")
        elif message.author.id == turn.id:
            damage = random.randint(1, 20)
            await asyncio.gather(processattack(message, damage))
            if mode == "17":
                return
            if turn == p1: other = p2
            else: other = p1
            other.hp -= damage
            await asyncio.gather(reporthp(message, str(damage))) #The order in which these occur matters.
            await asyncio.gather(checkstuff(message, damage))
            turn = other
            await message.channel.send("roll")

    if (message.content.lower() == "!quit" and (message.author.id == p1.id or message.author.id == p2.id)): #to abort the match
        embedVar = discord.Embed(title="The match between " + p1.tag.name + " and " + p2.tag.name + " has been aborted.", description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)), color=0x00ff00)
        embedVar.add_field(name="Have a nice day!", value="||(if this was an accident, please try !forceresume)||", inline=False)
        await message.channel.send(embed=embedVar) #match over and hp text
        await asyncio.gather(reportstats(message))
        """
        await message.channel.send("The match has been aborted.")
        await message.channel.send("The score is\n" + p1.name + " hp: " + str(p1.hp) + "\n" + p2.name + " hp: " + str(p2.hp))
        await message.channel.send("Stats:")
        await message.channel.send(p1.stats()) #Sends HP and stats
        await message.channel.send(p2.stats())
        """
        fighting = False

async def reportstats(message):
    global p1
    global p1
    embedVar = discord.Embed(title=(p1.tag.name + "'s stats:"), description=p1.stats(), color=0x00ff00)
    embedVar.set_thumbnail(url=(p1.tag.avatar_url)) #stats for player 1
    await message.channel.send(embed=embedVar)

    embedVar = discord.Embed(title=(p2.tag.name + "'s stats:"), description=p2.stats(), color=0x00ff00)
    embedVar.set_thumbnail(url=(p2.tag.avatar_url)) #stats for player 2
    await message.channel.send(embed=embedVar)

#runs after processattack
async def reporthp(message, damage):
    global p1
    global p2
    global turn
    embedVar = discord.Embed(title=(turn.tag.name + " did **" + damage + "** damage!"), description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)), color=0x00ff00)
    embedVar.set_author(name=(turn.tag.name + " roll"), icon_url=(turn.tag.avatar_url))
    await message.channel.send(embed=embedVar)

#Checks if the game is over, or if clash
async def checkstuff(message, damage):
    if turn == p2:
        if (p1.hp <= 0 and p2.hp <= 0):
            global mode
            mode = "draw"
            await message.channel.send("draw")
        elif (p1.hp <= 0 or p2.hp <= 0):
            embedVar = discord.Embed(title="The match between " + p1.tag.name + " and " + p2.tag.name + " has ended.", description=(p1.name + " HP: " + str(p1.hp) + "\n" + p2.name + " HP: " + str(p2.hp)), color=0x00ff00)
            await message.channel.send(embed=embedVar) #match over and hp text
            await asyncio.gather(reportstats(message))

#runs after someone rolls
async def processattack(message, dmg):
    global turn
    global damage
    if dmg == 1:
        embedVar = discord.Embed(title=("You got a one!!"), description="You miss your attack. *oof*", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        turn.ones += 1
        damage = 0
    elif dmg == luckies[turn.id]:
        embedVar = discord.Embed(title=("You got your lucky number!"), description="You heal 10HP.", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        turn.hp += 10
        turn.luckies += 1
        damage = luckies[turn.id]
    elif dmg == 17:
        embedVar = discord.Embed(title=("You got a 17!"), description="Would you like to `heal` or `attack`?\n(Attacking does 17 damage and healing rolls a 4d7.\nStats are only updated if you choose to heal.", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        global mode
        mode = "17"
        damage = 0
    elif dmg == 20:
        embedVar = discord.Embed(title=("You got a 20!"), description="||It doesn't do anything special, but your stats will be updated :pray:||", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        turn.twenties += 1
        damage = 20
    elif dmg == 30:
        embedVar = discord.Embed(title=("You got a 30!"), description="If you don't already have the award, please take care of that as I don't track awards.", color=0x00ff00)
        embedVar.set_author(name="Special Roll", icon_url=(turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)
        damage = 30

class Fighter:
    """ def __init__(self, tag):
        self.tag = tag #discord tag
        self.name = "<@" +str(self.id) + ">" #<@numbers>
        self.hp = PLAYERHP
        self.ones = 0
        self.twenties = 0
        self.luckies = 0
        self.seventeens = 0 """

    def reset(self, tag):
        self.tag = tag #discord tag
        self.id = self.tag.id
        #self.name = "<@" +str(self.id) + ">" #<@numbers>
        self.name = self.tag.name
        self.hp = PLAYERHP
        self.ones = 0
        self.twenties = 0
        self.luckies = 0
        self.seventeens = 0

    def stats(self):
        return (self.name + " got **" + str(self.ones) + "** ones, **" + str(self.twenties) + "** twenties,\n **" + str(self.luckies) + "** lucky numbers, and **" + str(self.seventeens) + "** seventeens.")

#Launch bot
with open('token.txt') as f:
    TOKEN = f.readline()
client.run(TOKEN)

#Reference

#wait:
#await asyncio.sleep(10)
#reply:
#await message.channel.reply('Hello!', mention_author=False)