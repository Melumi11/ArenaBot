#-------------------------------import----------------------------------#
import discord, logging
#-----------------------------------------------------------------------#

#-------------------------------variables-------------------------------#
client = discord.Client()
TOKEN = 'ODIyNDc0NzIxNTI1NjI4OTc5.YFSzRg.NE2o2SRi4Dr6XwBWDCuwQ0Ttv1M'
#-----------------------------------------------------------------------#
#python3 /Users/royhuang/Documents/GitHub/Fegg/Fegg.py

#Logging errors
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)
logging.basicConfig(level=logging.WARNING)

#Launch text in terminal
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Reading messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif ('kill me' or ('i' and 'die')) in message.content.lower():
        await message.channel.send("Please not worry. @everyone is here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/")
        await message.author.send('Please do not worry. We are here to help. If you are suicidal, you can find help at: https://suicidepreventionlifeline.org/')

    elif 'kill' in message.content.lower():
        await message.channel.send(":knife:")

    elif '...' in message.content.lower():
        await message.channel.send("** **")

    elif message.content.lower() == '!sweat':
        await message.channel.send("https://cdn.discordapp.com/attachments/822493563619246131/822498710873178133/unknown.png")
    
    elif ('fegg' in message.content.lower() and message.author.id == 640714673045504020):
        await message.channel.send("Greetings, most noble creator :feggbeg:")
    
    elif 'fegg' in message.content.lower():
        await message.channel.send('Hello!')

#Launch bot
client.run(TOKEN)

#Reference

#wait:
#await asyncio.sleep(10)