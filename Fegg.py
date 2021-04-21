# -------------------------------import----------------------------------#
import sys
import threading
from multiprocessing import Process

import discord
import logging
import random
import youtube_dl
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
# -----------------------------------------------------------------------#

# TODO: test automatic stat updating

# -------------------------------variables-------------------------------#
import Stathandler

TOKEN = ''  # Bot token
PLAYERHP = 100  # Starting health for both players
# -----------------------------------------------------------------------#

# Logging errors
logging.basicConfig(level=logging.ERROR)


# logging.basicConfig(level=logging.CRITICAL)
# logging.basicConfig(level=logging.WARNING) #Only the first one is actually used lol, me dum


# Handles main text reading and stuff


class MyClient(discord.Client):
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
        await client.change_presence(activity=activity)
        print(f'We have logged in as {self.user}')

    # Reading messages
    async def on_message(self, message):
        if message.author == client.user:  # so that the bot doesn't message itself
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
            if message_lower == '!sweat':
                await message.channel.send(
                    "https://cdn.discordapp.com/attachments/822493563619246131/822498710873178133/unknown.png")

            elif message_lower == '!help':  # help command
                embedVar = discord.Embed(title="Hi, my name is Fegg!",
                                         description="I am a bot coded by Melumi#5395. You can find my source code and fight rules at https://github.com/Melumi11/Fegg\nAll commands can be viewed by typing `/`\nFegg support server: https://discord.gg/fwUpkpCY5U",
                                         color=0x00ff00)
                embedVar.add_field(name=("List of commands:"),
                                   value="`!help` (this command)\n`/fight` (fight command for the Arena)\n`/sweat` (For the Colin Cult big-sweaters) ||Also `!sweat`||\n`/roll` (rolls a single die with up to a billion faces)\n`/setlucky` (sets your lucky number for Arena fights. Lasts until the bot is restarted (which can be often)) ||Also `!setlucky`||\n`/download` (given a link to a website with audio or video, fegg attempts to find a direct link using youtube-dl)",
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


class Fighter:  # Arena game player class
    def __init__(self, tag):
        self.tag = tag  # discord tag
        self.id = self.tag.id  # the long number
        # self.name = "<@" +str(self.id) + ">" #<@numbers>
        self.name = self.tag.name
        self.hp = PLAYERHP  # 100 by default, set at top
        self.ones = 0
        self.twenties = 0
        self.luckies = 0
        self.seventeens = 0
        self.clashwins = 0

        self.last = -1
        self.clash = 0
        self.rolls = []

    def stats(self):
        return f"{self.name} got **{self.ones}** ones, **{self.twenties}** twenties,\n**{self.luckies}** lucky numbers, **{self.seventeens}** seventeens, and **{self.clashwins}** clash wins."


class FightClass():
    def __init__(self, sender, target):
        self.mode = ""
        self.p1 = Fighter(sender)
        self.p2 = Fighter(target)
        self.turn = self.p1

    # Reading Messages, called by client class
    async def fight(self, message):  # Fight method
        if message.author == client.user:  # so that the bot doesn't message itself
            return

        if self.mode == "17":  # if the last roll was a 17
            if 'attack' in message.content.lower():  # attacks for 17
                if message.author.id == self.turn.id:
                    self.damage = 17  # damage is 17
                    if self.turn.id == self.p1.id:
                        self.other = self.p2  # Regular attacking biz
                    else:
                        self.other = self.p1
                    self.other.hp -= self.damage
                    await self.reporthp(message, str(self.damage))
                    self.turn = self.other  # switch turns
                    await self.checkstuff(message)
                    self.mode = ""  # not 17 anymore
                else:
                    await message.channel.send("Who are you?")
            if 'heal' in message.content.lower():  # heals for 4d7
                if message.author.id == self.turn.id:
                    self.damage = random.randint(1, 7) + random.randint(1, 7) + random.randint(1, 7) + random.randint(1,
                                                                                                                      7)  # rolls 4d7
                    self.turn.seventeens += 1  # update stats
                    self.turn.hp += self.damage  # heal
                    if self.turn.id == self.p1.id:
                        self.other = self.p2
                    else:
                        self.other = self.p1  # finds other player
                    # Instead of self.reporthp
                    embedVar = discord.Embed(title=(f"{self.turn.tag.name} healed **{self.damage}** health!"),
                                             description=(
                                                 f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"),
                                             color=0x00ff00)
                    embedVar.set_author(name=self.turn.tag.name, icon_url=(self.turn.tag.avatar_url))
                    await message.channel.send(embed=embedVar)
                    self.mode = ""  # not 17 anymore
                    self.turn = self.other  # change turn
                else:
                    await message.channel.send("Who are you?")

        if message.content.lower() == "roll":
            if self.mode == "17":  # if the last roll was 17 then don't roll
                await message.channel.send("Please choose whether to `heal` or `attack`.")
            elif self.mode == "clash":  # keep clashing
                await self.clash(message)
            elif message.author.id == self.turn.id:  # the person whose self.turn it is rolls
                if self.turn.id == self.p1.id:
                    self.other = self.p2
                else:
                    self.other = self.p1
                # Rolling the dice:
                if self.turn.id == self.p2.id: self.p2.hp += self.p1.last  # WARNING IDK IF THIS WILL WORK
                if self.other.hp - self.turn.hp >= 30:
                    await message.channel.send("Comeback rules activate! You roll a d30.")
                    self.damage = random.randint(1, 30)
                elif self.turn.hp <= 5:
                    if self.other.hp - self.turn.hp >= 25:
                        await message.channel.send("5HP comeback rules activate! You roll a d30.")
                        self.damage = random.randint(1, 30)
                # normal:
                else:
                    self.damage = random.randint(1, 20)
                if self.turn.id == self.p2.id: self.p2.hp -= self.p1.last  # END OF WARNING

                self.turn.rolls.append(self.damage)  # Tracks every roll
                if self.turn == self.p1:
                    self.p1.last = self.damage  # tracks last attack (do I need this? idk)
                    self.other = self.p2  # probably don't need this but whatevs
                else:
                    self.other = self.p1
                    if self.p1.last == self.damage:  # if self.p1's last is self.p2's current
                        self.mode = "clash"
                        self.other.hp -= self.damage
                        await self.clashstart(message, self.damage)  # doesn't self.reporthp, quits this function
                        return
                await self.processattack(message, self.damage)
                if self.mode == "17":  # not sure if this is needed
                    return
                self.other.hp -= self.damage
                await self.reporthp(message, str(self.damage))  # The order in which these occur matters.
                await self.checkstuff(message)  # checks if game is over
                self.turn = self.other

        if message.content.lower() == "!quit" and (
                message.author.id == self.p1.id or message.author.id == self.p2.id):  # to abort the match
            embedVar = discord.Embed(
                title=f"The match between {self.p1.tag.name} and {self.p2.tag.name} has been aborted.",
                description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"), color=0x00ff00)
            embedVar.add_field(name="Have a nice day!", value="||(if this was an accident, please try !forceresume)||",
                               inline=False)
            await message.channel.send(embed=embedVar)  # match over and hp text
            await self.reportstats(message)
            self.mode = ""
            self.endfight()  # END THE FIGHT

    # called when game ends
    async def reportstats(self, message):
        embedVar = discord.Embed(title=(self.p1.tag.name + "'s stats:"), description=self.p1.stats(), color=0x00ff00)
        embedVar.set_thumbnail(url=(self.p1.tag.avatar_url))  # stats for player 1
        await message.channel.send(embed=embedVar)

        embedVar = discord.Embed(title=(self.p2.tag.name + "'s stats:"), description=self.p2.stats(), color=0x00ff00)
        embedVar.set_thumbnail(url=(self.p2.tag.avatar_url))  # stats for player 2
        await message.channel.send(embed=embedVar)

    # runs after someone rolls
    async def processattack(self, message, dmg):
        if dmg == 1:  # self.damage = 0, updates stats
            embedVar = discord.Embed(title=("You got a one!!"), description="You miss your attack. *oof*",
                                     color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.turn.ones += 1
            self.damage = 0
        elif dmg == client.luckies[self.turn.id]:  # heals 10HP, updates stats
            embedVar = discord.Embed(title=("You got your lucky number!"), description="You heal 10HP.", color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.turn.hp += 10
            self.turn.luckies += 1
            self.damage = client.luckies[self.turn.id]
        elif dmg == 17:  # sets self.mode to 17, self.damage 0
            embedVar = discord.Embed(title=("You got a 17!"),
                                     description="Would you like to `heal` or `attack`?\n(Attacking does 17 damage and healing rolls a 4d7.\nStats are only updated if you choose to heal.",
                                     color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.mode = "17"
            self.damage = 0
        elif dmg == 20:  # updates stats
            embedVar = discord.Embed(title=("You got a 20!"),
                                     description="||It doesn't do anything special, but your stats will be updated :pray:||",
                                     color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.turn.twenties += 1
            self.damage = 20
        elif dmg == 30:  # special message
            embedVar = discord.Embed(title=("You got a 30!"),
                                     description="If you don't already have the award, please take care of that as I don't track awards.",
                                     color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.damage = 30

    # runs after processattack, after someone rolls
    async def reporthp(self, message, damage):
        embedVar = discord.Embed(title=(f"{self.turn.tag.name} did **{damage}** damage!"),
                                 description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"),
                                 color=0x00ff00)
        embedVar.set_author(name=(self.turn.tag.name + " roll"), icon_url=(self.turn.tag.avatar_url))
        await message.channel.send(embed=embedVar)

    # Checks if the game is over, including draw clash
    async def checkstuff(self, message):
        if self.turn == self.p2:
            if self.p1.hp <= 0 and self.p2.hp <= 0:  # draw
                embedVar = discord.Embed(
                    title=f"The match between {self.p1.tag.name} and {self.p2.tag.name} has ended in a draw.",
                    description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"), color=0x00ff00)
                embedVar.add_field(name=("Please update your stats with a draw."),
                                   value="If you would like to draw clash for the award, you can use `!roll d100` and win 3 out of 5 rolls.",
                                   inline=False)
                await message.channel.send(embed=embedVar)  # match over and hp text
                Stathandler.updatestats(self.p1.name, 2, self.p1.twenties, self.p1.ones, self.p1.luckies,
                                        self.p1.seventeens, self.p1.clashwins)
                Stathandler.updatestats(self.p2.name, 0, self.p2.twenties, self.p2.ones, self.p2.luckies,
                                        self.p2.seventeens, self.p2.clashwins)
                await self.reportstats(message)
                self.endfight()  # END THE FIGHT
                self.mode = ""
            elif self.p1.hp <= 0 or self.p2.hp <= 0:
                embedVar = discord.Embed(
                    title=f"The match between {self.p1.tag.name} and {self.p2.tag.name} has ended.",
                    description=f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}\nPlease update your stats and awards, and try to remember as I can't check all of them.",
                    color=0x00ff00)
                await message.channel.send(embed=embedVar)  # match over and hp text
                if self.p1.hp <= 0:
                    Stathandler.updatestats(self.p1.name, 1, self.p1.twenties, self.p1.ones, self.p1.luckies,
                                            self.p2.seventeens, self.p1.clashwins)
                    Stathandler.updatestats(self.p2.name, 0, self.p2.twenties, self.p2.ones, self.p2.luckies,
                                            self.p2.seventeens, self.p2.clashwins)
                else:
                    Stathandler.updatestats(self.p1.name, 0, self.p1.twenties, self.p1.ones, self.p1.luckies,
                                            self.p2.seventeens, self.p1.clashwins)
                    Stathandler.updatestats(self.p2.name, 1, self.p2.twenties, self.p2.ones, self.p2.luckies,
                                            self.p2.seventeens, self.p2.clashwins)
                await self.reportstats(message)
                self.mode = ""
                if self.p1.hp == 0 or self.p2.hp == 0:
                    embedVar = discord.Embed(title=("You finished your opponent with the exact number!"),
                                             description="You can get an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp == 1 or self.p2.hp == 1:
                    embedVar = discord.Embed(title=("You finished your opponent with 1 HP remaining!"),
                                             description="You can get an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp <= -15 or self.p2.hp <= -15:
                    embedVar = discord.Embed(title=("You finished your opponent to -15 HP!"),
                                             description="You may be eligible for an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp >= 30 or self.p2.hp >= 30:
                    embedVar = discord.Embed(title=("You finished your opponent with 30 health left!"),
                                             description="You can get an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp >= 50 or self.p2.hp >= 50:
                    embedVar = discord.Embed(title=("You finished your opponent with 50 health left!"),
                                             description="You can get an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if self.p1.hp >= 70 or self.p2.hp >= 70:
                    embedVar = discord.Embed(title=("You finished your opponent with 70 health left!"),
                                             description="You can get an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if (self.p1.rolls[0] == 20 and self.p2.rolls[0] == 1) or (
                        self.p2.rolls[0] == 20 and self.p2.rolls[0] == 1):
                    embedVar = discord.Embed(title=("Your first roll was a 20 and your opponent's was a miss!"),
                                             description="You can get an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if (self.p1.rolls[-1] == client.luckies[self.p1.id]) or (
                        self.p2.rolls[-1] == client.luckies[self.p2.id]):
                    embedVar = discord.Embed(title=("You finished your opponent with your lucky number!"),
                                             description="You can get an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                if (self.p1.rolls[-1] == 20) or (self.p2.rolls[-1] == 20):
                    embedVar = discord.Embed(title=("You finished your opponent with a special attack!"),
                                             description="You can get an award if you don't already have it.",
                                             color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                self.endfight()  # END THE FIGHT
        for i in {self.p1, self.p2}:  # 3 in a row
            if len(i.rolls) > 2 and i.rolls[-1] == i.rolls[-2] and i.rolls[-2] == i.rolls[-3]:
                embedVar = discord.Embed(title=("You got three in a row!"),
                                         description="You get a bonus attack! You can also claim an award if you don't already have it :D",
                                         color=0x00ff00)
                embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
                await message.channel.send(embed=embedVar)
                self.turn = i
        if (self.p1.hp >= 125) or (self.p2.hp >= 125):
            embedVar = discord.Embed(title=("You have over 125 health!"),
                                     description="You can get an award if you don't already have it.", color=0x00ff00)
            await message.channel.send(embed=embedVar)

    # Start clash text, sets self.turn to self.p1
    async def clashstart(self, message, damage):
        embedVar = discord.Embed(title=("Clash!"), description="Both players got a " + str(damage), color=0x00ff00)
        embedVar.add_field(name="Both players will now roll d100s",
                           value="You need to win two out of three rolls.\n" + self.p1.name + " goes first.",
                           inline=False)
        await message.channel.send(embed=embedVar)
        self.turn = self.p1

    # Processes clash rolls
    async def clash(self, message):
        if message.author.id == self.turn.id:
            # code.interact(local=locals())
            self.damage = random.randint(1, 100)
            winner = None  # init winner
            if self.damage == 1:  # sets self.other person's clash score to 2 and says you lose
                if self.turn.id == self.p1.id:
                    self.p2.clash = 2
                else:
                    self.p1.clash = 2
                await message.channel.send("You automatically lose the clash. oof.")
            if self.damage == 100:  # sets clash score to 2, mentions award
                self.turn.clash = 2
                await message.channel.send(
                    "You automatically win the clash. If you don't already have the award, please claim it now.")

            if not winner and self.turn.id == self.p1.id:  # cuz turn is backwards
                self.p2.last = self.damage  # for checking who won the round
            else:  # self.turn is self.p2, time to check stuff
                if self.damage > self.p2.last:
                    self.p2.clash += 1  # checks who won the clash
                elif self.damage < self.p2.last:
                    self.p1.clash += 1
                else:
                    await message.channel.send(
                        "wtf you got the same number and idk what to do so I won't count this one")
                if self.p1.clash >= 2:
                    winner = self.p1
                elif self.p2.clash >= 2:
                    winner = self.p2
                if winner and winner.clash >= 2:  # winner text and stuff, quits function
                    await message.channel.send(f"{self.turn.tag.name} got a **{self.damage}**!!")
                    winner.hp += self.p1.last
                    embedVar = discord.Embed(title=(winner.tag.name + " won the clash!"),
                                             description=f"The clash score is:\n{self.p1.name}: {self.p1.clash}\n{self.p2.name}: {self.p2.clash}",
                                             color=0x00ff00)
                    embedVar.set_thumbnail(url=(winner.tag.avatar_url))
                    await message.channel.send(embed=embedVar)
                    await self.reporthp(message, self.p1.last)
                    self.mode = ""
                    self.p2.last = -1
                    self.turn = self.p1
                    winner.clashwins += 1
                    winner = None
                    self.p1.clash, self.p2.clash = 0, 0
                    return

            embedVar = discord.Embed(title=(f"{self.turn.tag.name} got a **{self.damage}**!!"), description=(
                f"The clash score is:\n{self.p1.name}: {self.p1.clash}\n{self.p2.name}: {self.p2.clash}"),
                                     color=0x00ff00)
            embedVar.set_author(name=(self.turn.tag.name + " roll"), icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)  # Reports roll
            if self.turn.id == self.p1.id:
                self.turn = self.p2
            else:
                self.turn = self.p1

    def endfight(self):
        client.current_fighters.remove(self.p1.id)
        client.current_fighters.remove(self.p2.id)
        for i in client.current_fights:
            if i.p1.id == self.p1.id:
                client.current_fights.remove(i)
    # When game is over: current_fighters.remove() both players


# -----------------------------Slash Commands----------------------------#
client = MyClient()  # MyClient()
slash = SlashCommand(client, sync_commands=True)  # Declares slash commands through the client.


# Roll
@slash.slash(name="roll", description="Dice roll command, up to 999,999,999",
             options=[create_option(
                 name="d",
                 description="Roll a d-sided die",
                 option_type=3,
                 required=True)])
async def roll(ctx, d):
    if len(d) < 17:  # dice roll command (up to 999,999,999)
        try:
            await ctx.send(content=f"Roll d{d}: `[{str(random.randint(1, int(d)))}]`")
        except:
            await ctx.send(content="Please enter a number between zero and one billion")


# Stats
@slash.slash(name="setstats", description="Add statistics",
             options=[
                 create_option(
                     name="Special",
                     description="Your special attack.",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="Weapon",
                     description="Your weapon.",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="Lucky",
                     description="Your lucky number. This cant be 1, 17, 20, or another players number.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Games",
                     description="Total amount of games you've played.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Wins",
                     description="Total amount of games won.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Losses",
                     description="Total amount of games lost.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Draws",
                     description="Total amount of games ended with a draw.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Ones",
                     description="Total amount of ones rolled.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Twenties",
                     description="Total amount of twenties rolled.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Luckies",
                     description="Total amount of lucky numbers rolled.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Seventeens",
                     description="Total amount of times seventeen was rolled and used to heal rather than damage.",
                     option_type=4,
                     required=True
                 ),
                 create_option(
                     name="Clashes",
                     description="Total amount of clashes won.",
                     option_type=4,
                     required=True
                 )
             ])
async def setstats(ctx, special, weapon, lucky, games, wins, losses, draws, ones, twenties, luckies, seventeens,
                   clashes):
    Stathandler.write(ctx.author.id, special, weapon, lucky, games, wins, losses, draws, ones, twenties, luckies,
                      seventeens, clashes)
    await ctx.send("Your statistics have been updated!")


@slash.slash(name="stats", description="Check a fighter's statistics.",
             options=[
                 create_option(
                     name="Fighter",
                     description="The fighter to check.",
                     option_type=6,
                     required=True
                 )
             ])
async def stats(ctx, fighter):
    fstats = Stathandler.read(fighter.id)
    if fstats["fnf"]:
        embed = discord.Embed(
            title=ctx.author.name + " doesn't seem to have any statistics.",
            description="If you're" + ctx.author.name + ", use /setstats to set your statistics!",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=fighter.name + "'s Statistics",
            description="If you're " + fighter.name + " and want to change these, use /setstats to set your statistics!",
            colour=0x00ff00
        )
        embed.add_field(
            name="Special Attack:",
            value=fstats["special"],
            inline=False
        )
        embed.add_field(
            name="Weapon:",
            value=fstats["weapon"],
            inline=False
        )
        embed.add_field(
            name="Lucky Number:",
            value=fstats["lucky"],
            inline=False
        )
        embed.add_field(
            name="Total Fights:",
            value=fstats["total"],
            inline=False
        )
        embed.add_field(
            name="Wins:",
            value=str(fstats["wins"]),
            inline=False
        )
        embed.add_field(
            name="Losses:",
            value=str(fstats["losses"]),
            inline=False
        )
        embed.add_field(
            name="Draws:",
            value=str(fstats["draws"]),
            inline=False
        )
        embed.add_field(
            name="1s Rolled:",
            value=str(fstats["ones"]),
            inline=False
        )
        embed.add_field(
            name="20s Rolled:",
            value=str(fstats["twenties"]),
            inline=False
        )
        embed.add_field(
            name="Lucky Numbers Rolled:",
            value=str(fstats["luckies"]),
            inline=False
        )
        embed.add_field(
            name="Seventeens Used For Healing:",
            value=str(fstats["seventeens"]),
            inline=False
        )
        embed.add_field(
            name="Clashes:",
            value=str(fstats["clashes"]),
            inline=False
        )
        await ctx.send(embed=embed)


# Fight
@slash.slash(name="fight", description="Fight with another user according to the standard Arena rules.",
             options=[create_option(
                 name="Target",
                 description="Please @ the user who you would like to fight with.",
                 option_type=6,
                 required=True)])
async def fight(ctx, target):
    # Checks if they are already fighting:
    if ctx.author.id in client.current_fighters:
        await ctx.send("You can't fight two people at once.")
        return

    if target.id in client.current_fighters:
        await ctx.send(target.name + " is already in a fight.")
        return

    if ctx.author == target:
        await ctx.send("You can't fight yourself.")
        return

    # checking to see both players' lucky numbers are registered
    try:
        client.luckies[ctx.author.id]
    except KeyError:
        await ctx.send(
            f"Uh oh, {ctx.author.name}'s lucky number is not in my database. Please ask Melumi#5395 for help.\nYou can also use `/setlucky` to temporarily set your lucky number to fight.")
        await ctx.send(
            f"Uh oh, {ctx.author.name}'s lucky number is not in my database. \nYou can use `/setlucky` to temporarily set your lucky number to fight.")
        return
    try:
        client.luckies[target.id]
    except KeyError:
        await ctx.send(
            f"Uh oh, {target.name}'s lucky number is not in my database. Please ask Melumi#5395 for help.\nYou can also use `/setlucky` to temporarily set your lucky number to fight.")
        await ctx.send(
            f"Uh oh, {target.name}'s lucky number is not in my database. \nYou can use `/setlucky` to temporarily set your lucky number to fight.")
        return

    # Create an instance of the FightClass
    # str(ctx.author.id) = FightClass(ctx.author, target)

    # Add them to the list of fighters
    client.current_fighters.append(ctx.author.id)
    client.current_fighters.append(target.id)
    client.current_fights.append(FightClass(ctx.author, target))

    embedVar = discord.Embed(title=(f"**{ctx.author.name}** challenges **{target.name}** to a battle!"),
                             description="The first player to lose all their health loses.", color=0x00ff00)
    embedVar.add_field(name=(
        f"**{ctx.author.name}**'s lucky number is {client.luckies[ctx.author.id]} and **{target.name}**'s is {client.luckies[target.id]}."),
        value=("Type `roll` to attack and `!quit` to stop fighting."), inline=False)
    embedVar.set_thumbnail(url=(ctx.author.avatar_url))
    await ctx.send(embed=embedVar)


# Sweat
@slash.slash(name="sweat", description=":colinsweat:")
async def sweat(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/822493563619246131/822498710873178133/unknown.png")


# Setlucky
@slash.slash(name="setlucky", description="Temporarily set your lucky number.",
             options=[create_option(
                 name="Lucky",
                 description="Choose a number between 1 and 20.",
                 option_type=4,
                 required=True)])
async def roll(ctx, Lucky):
    if ctx.author.id in client.luckies.keys():
        await ctx.send("Your lucky number is already set as " + str(client.luckies[ctx.author.id]))
    elif 1 <= Lucky <= 20:
        client.luckies[ctx.author.id] = Lucky
        await ctx.send(
            "Your lucky number has been set as " + str(client.luckies[ctx.author.id]) + " until the bot is restarted.")
    else:
        await ctx.send("Please choose a number between 1 and 20 (inclusive)")


# Download
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [my_hook]}


@slash.slash(name="download",
             description="Find a media file, given a link. Use this if you want to quickly download something.",
             options=[create_option(
                 name="Source",
                 description="Link to the media you want to find.",
                 option_type=3,
                 required=True)])
async def audio(ctx, Source):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            r = ydl.extract_info(Source, download=False)
            await ctx.send(r['url'])
        except Exception as exception:
            await ctx.send(f"**{type(exception).__name__}**: `{str(exception)[18:-89]}`")


# -----------------------------------------------------------------------#

# -------------------------------Launch bot------------------------------#
with open('token.txt') as f:
    TOKEN = f.readline()
client.run(TOKEN)

# Reference

# wait:
# await asyncio.sleep(10)
# reply:
# await message.channel.reply('Hello!', mention_author=False)

# Very cool debug command that stops the script and shows all variables, can resume after
# import code
# code.interact(local=locals())
