import discord
import Stathandler

class Client(discord.Client):
    # -------------------------------"Global" Variables:-------------------------------#
    luckies = Stathandler.readluckies()
    MELUMI = 640714673045504020  # my discord id
    # For fight game:
    current_fighters = []
    current_fights = []

    # ----------------------------------------------------------------------------------#
    # Launch text in terminal
    async def on_ready(self):  # login text, init fighters, self.turn = self.p1
        activity = discord.Activity(type=discord.ActivityType.competing,
                                    name="the Arena")  # Playing, Listening to, Watching, also streaming, competing
        await self.change_presence(activity=activity)
        print(f'We have logged in as {self.user}')

    # Reading messages
    async def on_message(self, message):
        if message.author == self.user:  # so that the bot doesn't message itself
            return

        # Going through the fight functions
        try:
            for i in range((len(self.current_fights))):
                await self.current_fights[i].fight(message)
        except IndexError:
            for i in range((len(self.current_fights))):
                await self.current_fights[i].fight(message)

        message_lower = message.content.lower()  # converts message to lowercase (cuz it's used a lot)
        if message_lower.startswith('!'):
            if message_lower == '!help':  # help command
                embedVar = discord.Embed(title="Hi, my name is ArenaBot!",
                                         description="I am a bot coded by Melumi#5395. You can find my source code and fight rules at https://github.com/Melumi11/ArenaBot\nAll commands can be viewed by typing `/`\nArenaBot Support Server: https://discord.gg/fwUpkpCY5U",
                                         color=0x00ff00)
                embedVar.add_field(name=("List of commands:"),
                                   value="`!help` (this command)\n`/fight` (fight command for the Arena)\n`/roll` (rolls a single die with up to a billion faces)\n`/setlucky` (sets your lucky number for Arena fights. Lasts until the bot is restarted (which can be often)) ||Also `!setlucky`||",
                                   inline=False)
                await message.channel.send(embed=embedVar)

            elif message_lower.startswith("!setlucky"):
                if message.author.id in self.luckies.keys():
                    await message.channel.send(
                        "Your lucky number is already set as " + str(self.luckies[message.author.id]))
                elif len(message.content) <= 10:
                    await message.channel.send(
                        "Please type the command like `!setlucky 1` or `!setlucky 11`. You can also use !setlucky for more help.")
                else:
                    if message.content[10:].isdigit():
                        num = message.content[10:]
                        if 0 < int(num) <= 20:
                            self.luckies[message.author.id] = num
                            await message.channel.send("Your lucky number has been set as " + str(
                                self.luckies[message.author.id]) + " until the bot is restarted.")
                        else:
                            await message.channel.send(
                                "Please use a number between 1 and 20 such as `!setlucky 11`. You can also use /setlucky for more help")

            elif message_lower.startswith("!fight"):
                await message.channel.send("please use `/fight` if you would like to fight.")

        elif 'parm' in message_lower:  # parm
            await message.channel.send("https://images.heb.com/is/image/HEBGrocery/000081264")
            await message.author.send("https://images.heb.com/is/image/HEBGrocery/000081264")
            #hehe
