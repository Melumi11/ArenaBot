import discord
import random
import stathandler

class Fighter:  # Arena game player class
    def __init__(self, tag, PLAYERHP):
        self.tag = tag  # discord tag
        self.id = self.tag.id  # the long number
        # self.name = "<@" +str(self.id) + ">" #<@numbers>
        self.name = self.tag.name
        self.hp = PLAYERHP  # 100 by default, set at top of Main 
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
    def __init__(self, sender, target, client, PLAYERHP, channel):
        self.mode = ""
        self.p1 = Fighter(sender, PLAYERHP)
        self.p2 = Fighter(target, PLAYERHP)
        self.turn = self.p1
        self.client = client
        # Channel checking for statistic updating
        self.channel = channel
        self.officialFights1 = 796200467146735646
        self.officialFights2 = 796478745724715049

    # Reading Messages, called by self.client class
    async def fight(self, message):  # Fight method
        if message.author == self.client.user:  # so that the bot doesn't message itself
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
                description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}\n\nHave a nice day!"), color=0x00ff00)
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
        elif dmg == self.client.luckies[self.turn.id]:  # heals 10HP, updates stats
            embedVar = discord.Embed(title=("You got your lucky number!"), description="You heal 10HP.", color=0x00ff00)
            embedVar.set_author(name="Special Roll", icon_url=(self.turn.tag.avatar_url))
            await message.channel.send(embed=embedVar)
            self.turn.hp += 10
            self.turn.luckies += 1
            self.damage = self.client.luckies[self.turn.id]
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
            if self.p1.hp <= 0 or self.p2.hp <= 0 and self.p1.hp == self.p2.hp:  # draw
                embedVar = discord.Embed(
                    title=f"The match between {self.p1.tag.name} and {self.p2.tag.name} has ended in a draw.",
                    description=(f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}"), color=0x00ff00)
                embedVar.add_field(name=("Your draw stat has been updated."),
                                   value="If you would like to draw clash for the award, you can use `!roll d100` and win 3 out of 5 rolls.",
                                   inline=False)
                await message.channel.send(embed=embedVar)  # match over and hp text
                if self.channel == self.officialFights1 or self.channel == self.officialFights2:
                    stathandler.updatestats(self.p1.id, 2, self.p1.twenties, self.p1.ones, self.p1.luckies,
                                        self.p1.seventeens, self.p1.clashwins)
                    stathandler.updatestats(self.p2.id, 2, self.p2.twenties, self.p2.ones, self.p2.luckies,
                                        self.p2.seventeens, self.p2.clashwins)

                await self.reportstats(message)
                self.endfight()  # END THE FIGHT
                self.mode = ""
            elif self.p1.hp <= 0 or self.p2.hp <= 0:
                embedVar = discord.Embed(
                    title=f"The match between {self.p1.tag.name} and {self.p2.tag.name} has ended.",
                    description=f"{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}\nYour stats have been updated, but you need to update your awards.",
                    color=0x00ff00)
                await message.channel.send(embed=embedVar)  # match over and hp text
                if self.channel == self.officialFights1 or self.channel == self.officialFights2:
                    if self.p1.hp < self.p2.hp:
                        stathandler.updatestats(self.p1.id, 1, self.p1.twenties, self.p1.ones, self.p1.luckies,
                                                self.p2.seventeens, self.p1.clashwins)
                        stathandler.updatestats(self.p2.id, 0, self.p2.twenties, self.p2.ones, self.p2.luckies,
                                                self.p2.seventeens, self.p2.clashwins)
                    else:
                        stathandler.updatestats(self.p1.id, 0, self.p1.twenties, self.p1.ones, self.p1.luckies,
                                                self.p2.seventeens, self.p1.clashwins)
                        stathandler.updatestats(self.p2.id, 1, self.p2.twenties, self.p2.ones, self.p2.luckies,
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
                if (self.p1.rolls[-1] == self.client.luckies[self.p1.id]) or (
                        self.p2.rolls[-1] == self.client.luckies[self.p2.id]):
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
            if not winner and self.turn.id == self.p1.id: # sets p1's attack to p2.last
                self.p2.last = self.damage  # for checking who won the round
            else:  # self.turn is self.p2, time to check stuff
                if self.damage > self.p2.last: # if p2's attack is greater than p1's attack
                    self.p2.clash += 1 
                elif self.damage < self.p2.last:
                    self.p1.clash += 1
                else:
                    await message.channel.send(
                        "you got the same number and idk what to do so I won't count this one")
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
                    await message.channel.send(f"{winner.name} has done the {self.p1.last} damage.\n{self.p1.name} HP: {self.p1.hp}\n{self.p2.name} HP: {self.p2.hp}")
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
        self.client.current_fighters.remove(self.p1.id)
        self.client.current_fighters.remove(self.p2.id)
        for i in self.client.current_fights:
            if i.p1.id == self.p1.id:
                self.client.current_fights.remove(i)
    # When game is over: current_fighters.remove() both players
