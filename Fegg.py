#-------------------------------import----------------------------------#
import discord
#-----------------------------------------------------------------------#

#-------------------------------variables-------------------------------#
client = discord.Client()
TOKEN = 'ODIyNDc0NzIxNTI1NjI4OTc5.YFSzRg.NE2o2SRi4Dr6XwBWDCuwQ0Ttv1M'
#-----------------------------------------------------------------------#
#python3 /Users/royhuang/Documents/GitHub/Fegg/Fegg.py

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    elif 'kill' in message.content.lower():
        await message.channel.send(":knife:")

    elif '...' in message.content.lower():
        await message.channel.send("** **")

    elif message.content.lower() == '!sweat':
        await message.channel.send("<:colinsweat:822487253758640158><:colinsweat:822487253758640158><:colinsweat:822487253758640158>")
    
    elif message.author.id == 640714673045504020:
        await message.channel.send("Hello Melumi")

#Launch bot
client.run(TOKEN)