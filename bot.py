# -------------------------------import----------------------------------#
import select
import sys
import tty
import termios

import discord
import logging
import random
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

# My Classes
from client import * # Main class responsible for reading messages and stuff
from fight import * # Fighter class and FightClass which handles the fights
# -----------------------------------------------------------------------#


# -------------------------------variables-------------------------------#
import Stathandler

TOKEN = ''  # Bot token
PLAYERHP = 100  # Starting health for both players
# -----------------------------------------------------------------------#

# Logging errors
logging.basicConfig(level=logging.ERROR)


# -----------------------------Slash Commands----------------------------#
client = Client()  # MyClient()
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
    await ctx.send("Your stats have been updated!")


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
                 description="Please choose the user who you would like to fight with.",
                 option_type=6,
                 required=True)])
async def fight(ctx, target):
    print(ctx.author)
    print(target)
    # Checks if they are already fighting:
    if ctx.author.id in client.current_fighters:
        await ctx.send("You can't fight two people at once.")
        return

    try:
        if target.id in client.current_fighters:
            await ctx.send(target.name + " is already in a fight.")
            return
    except Exception as exception:
        await ctx.send(f"An error has occured: `{exception}`. \nThis might be because you are in a dm but I'm not sure. If something is wrong, please notify Melumi#5395 in chat or in the official support server (!help)")
        return
    
    if ctx.author.id == target.id:
        await ctx.send("You can't fight yourself.")
        return

    # checking to see both players' lucky numbers are registered
    try:
        client.luckies[ctx.author.id]
    except KeyError:
        await ctx.send(
            f"Uh oh, {ctx.author.name}'s lucky number is not in my database. \nYou can use `/setlucky` to temporarily set your lucky number to fight, and `/setstats` to set your stats permanently, including lucky number.")
        return
    try:
        client.luckies[target.id]
    except KeyError:
        await ctx.send(
            f"Uh oh, {target.name}'s lucky number is not in my database. \nYou can use `/setlucky` to temporarily set your lucky number to fight, and `/setstats` to set your stats permanently, including lucky number.")
        return

    # Create an instance of the FightClass
    # str(ctx.author.id) = FightClass(ctx.author, target)

    # Add them to the list of fighters
    client.current_fighters.append(ctx.author.id)
    client.current_fighters.append(target.id)
    client.current_fights.append(FightClass(ctx.author, target, client, PLAYERHP))

    embedVar = discord.Embed(title=(f"**{ctx.author.name}** challenges **{target.name}** to a battle!"),
                             description="The first player to lose all their health loses.", color=0x00ff00)
    embedVar.add_field(name=(
        f"**{ctx.author.name}**'s lucky number is {client.luckies[ctx.author.id]} and **{target.name}**'s is {client.luckies[target.id]}."),
        value=("Type `roll` to attack and `!quit` to stop fighting."), inline=False)
    embedVar.set_thumbnail(url=(ctx.author.avatar_url))
    await ctx.send(embed=embedVar)


# Setlucky
@slash.slash(name="setlucky", description="Temporarily set your lucky number.",
             options=[create_option(
                 name="lucky",
                 description="Choose a number between 1 and 20.",
                 option_type=4,
                 required=True)])
async def roll(ctx, lucky):
    if ctx.author.id in client.luckies.keys():
        await ctx.send("Your lucky number is already set as " + str(client.luckies[ctx.author.id]))
    elif 1 <= lucky <= 20:
        client.luckies[ctx.author.id] = lucky
        await ctx.send(
            "Your lucky number has been set as " + str(client.luckies[ctx.author.id]) + " until the bot is restarted.")
    else:
        await ctx.send("Please choose a number between 1 and 20 (inclusive)")


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
