#-------------------------------import----------------------------------#
import discord, logging, asyncio
#-----------------------------------------------------------------------#

#-------------------------------variables-------------------------------#
client = discord.Client()
TOKEN = 'ODIyNDc0NzIxNTI1NjI4OTc5.YFSzRg.NE2o2SRi4Dr6XwBWDCuwQ0Ttv1M'
luckies = {822474721525628979: 1, 259716396198395904: 2, 543857545278783520: 3, 400514653957914635: 4, 246080207704817664: 5, 567819726013726722: 6, 332711880831270912: 7, 320559692269223938: 8, 194310041900154880: 9, 548617575282769922: 10, 640714673045504020: 11, 175824478423482368: 13, 294736827946893313: 16, 748751242003611739: 18, 731368690364186634: 19}
fighting = False
p1, p2 = None, None
PLAYERHP = 100
#-----------------------------------------------------------------------#

#Logging errors
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)
logging.basicConfig(level=logging.WARNING)

#Launch text in terminal
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #Initialize players
    global p1
    global p2
    p1 = Fighter()
    p2 = Fighter()

#Reading messages
@client.event
async def on_message(message):
    global fighting #takes fighting status variable
    if message.author == client.user: #so that the bot doesn't message itself
        return
    
    if fighting == True: #If people are fighting then we call fight
        await asyncio.gather(fight(message))

    if message.content.startswith("!fight"): #begin fight if no one is fighting
        if fighting == False:
            await asyncio.gather(startfight(message))
        else:
            await message.channel.send("There is already a fight going on between " + str(p1.tag) + " and " + str(p2.tag) + " and the maker of this bot did not anticipate that he needed to add code for more than one battle at a time. Please contact Melumi#5395 or ask the current fighters to wrap up or quit their game. Thank you.")
        
    elif ('kill me' or ('i' and 'die')) in message.content.lower(): #suicide prevention
        await message.channel.send("Please not worry. @everyone is here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/")
        await message.author.send('Please do not worry. We are here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/')

    elif 'kill' in message.content.lower(): #knife emoji
        await message.channel.send(":knife:")

    elif '...' in message.content.lower(): #blank message
        await message.channel.send("** **")

    elif message.content.lower() == '!sweat': #big sweat
        await message.channel.send("https://cdn.discordapp.com/attachments/822493563619246131/822498710873178133/unknown.png")
    
    elif ('fegg' in message.content.lower() and message.author.id == 640714673045504020): #my text
        await message.channel.send("Greetings, most noble creator <:fleggbeg:800558355714015263>")
    
    elif 'fegg' in message.content.lower(): #greetings
        await message.channel.send('Hello!')

async def startfight(message): #called when a fight starts
    global fighting
    global p1 #gets player variables
    global p2 #fighting = False
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
                await message.channel.send(p1.name + " challenges " + p2.name + " to a battle!") #if no errors, the battle text comes
                await message.channel.send("The first person to lose all their health loses.")
                await message.channel.send("Type `roll` to attack and `!quit` to stop fighting.")
                await message.channel.send(p1.name + "'s lucky number is " + str(luckies[p1.id]) + " and " + p2.name + "'s is " + str(luckies[p2.id]))
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
    if (message.content.lower() == "!quit" and (message.author.id == p1.id or message.author.id == p2.id)): #to abort the match
        await message.channel.send("The match has been aborted.")
        await message.channel.send("The score is\n" + p1.name + " hp: " + str(p1.hp) + "\n" + p2.name + " hp: " + str(p2.hp))
        await message.channel.send("Stats:")
        await message.channel.send(p1.stats())
        await message.channel.send(p2.stats())
        print("hello")
        fighting = False

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
        self.name = "<@" +str(self.id) + ">" #<@numbers>
        self.hp = PLAYERHP
        self.ones = 0
        self.twenties = 0
        self.luckies = 0
        self.seventeens = 0

    def stats(self):
        return (self.name + " got **" + str(self.ones) + "** ones, **" + str(self.twenties) + "** twenties, **" + str(self.luckies) + "** lucky numbers, and **" + str(self.seventeens) + "** seventeens.")

#Launch bot
client.run(TOKEN)

#Reference

#wait:
#await asyncio.sleep(10)