import random
from discord_slash.utils.manage_commands import create_option
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType
import stathandler
import discord
from fight import FightClass
# For select/dropdown:
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, ComponentContext
from discord.ext import commands

def roll():
    description = "Dice roll command, up to 999,999,999"
    options=[create_option(
                    name="d",
                    description="Roll a d-sided die",
                    option_type=SlashCommandOptionType.INTEGER,
                    required=True)]
    
    @slash.slash(name="roll", description=description, options=options)
    async def roll(ctx, d):
        if 0 < d <= 999999999:  # dice roll command (up to 999,999,999)
            await ctx.send(content=f"Roll d{d}: `[{str(random.randint(1, d))}]`")
        else:
            await ctx.send(content="Please enter a number between one and one billion")


def setstats():
    description="Add statistics"
    options=[create_option(
                        name="special",
                        description="Your special attack.",
                        option_type=SlashCommandOptionType.STRING,
                        required=True
                    ),
                    create_option(
                        name="weapon",
                        description="Your weapon.",
                        option_type=SlashCommandOptionType.STRING,
                        required=True
                    ),
                    create_option(
                        name="lucky",
                        description="Your lucky number. This cant be 1, 17, 20, or another players number.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="games",
                        description="Total amount of games you've played.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="wins",
                        description="Total amount of games won.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="losses",
                        description="Total amount of games lost.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="draws",
                        description="Total amount of games ended with a draw.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="ones",
                        description="Total amount of ones rolled.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="twenties",
                        description="Total amount of twenties rolled.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="luckies",
                        description="Total amount of lucky numbers rolled.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="seventeens",
                        description="Total amount of times seventeen was rolled and used to heal rather than damage.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    ),
                    create_option(
                        name="clashes",
                        description="Total amount of clashes won.",
                        option_type=SlashCommandOptionType.INTEGER,
                        required=True
                    )]

    @slash.slash(name="setstats", description=description, options=options)
    async def setstats(ctx, special, weapon, lucky, games, wins, losses, draws, ones, twenties, luckies, seventeens, clashes):
        if "," in str(special):
            await ctx.send("Your stats cant have commas in them!")
        else:
            stathandler.write(ctx.author.id, special, weapon, lucky, games, wins, losses, draws, ones, twenties, luckies, seventeens, clashes)
            client.luckies[ctx.author.id] = lucky
            await ctx.send("Your stats have been updated!")


def stats():
    description="Check a fighter's statistics."
    options=[create_option(
                        name="fighter",
                        description="The fighter to check.",
                        option_type=SlashCommandOptionType.USER,
                        required=True
                    )
                ]

    @slash.slash(name="stats", description=description, options=options)
    async def stats(ctx, fighter):
        fullstats = stathandler.read(fighter.id)
        if not fullstats[0]:
            embed = discord.Embed(
                title=ctx.author.name + " doesn't seem to have any statistics.",
                description="If you're " + fighter.name + " and want to change these, use /setstats to set your statistics!",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            fstats = fullstats[1]
            embed = discord.Embed(
                title=fighter.name + "'s Statistics",
                description="If you're " + fighter.name + " and want to change these, use /setstats to set your statistics!",
                colour=0x00ff00
            )
            embed.add_field(
                name="Special Attack:",
                value=fstats[1],
                inline=False
            )
            embed.add_field(
                name="Weapon:",
                value=fstats[2],
                inline=False
            )
            embed.add_field(
                name="Lucky Number:",
                value=fstats[3],
                inline=False
            )
            embed.add_field(
                name="Total Fights:",
                value=fstats[4],
                inline=False
            )
            embed.add_field(
                name="Wins:",
                value=str(fstats[5]),
                inline=False
            )
            embed.add_field(
                name="Losses:",
                value=str(fstats[6]),
                inline=False
            )
            embed.add_field(
                name="Draws:",
                value=str(fstats[7]),
                inline=False
            )
            embed.add_field(
                name="1s Rolled:",
                value=str(fstats[8]),
                inline=False
            )
            embed.add_field(
                name="20s Rolled:",
                value=str(fstats[9]),
                inline=False
            )
            embed.add_field(
                name="Lucky Numbers Rolled:",
                value=str(fstats[10]),
                inline=False
            )
            embed.add_field(
                name="Seventeens Used For Healing:",
                value=str(fstats[11]),
                inline=False
            )
            embed.add_field(
                name="Clashes:",
                value=str(fstats[12]),
                inline=False
            )
            await ctx.send(embed=embed)


def fight():
    description="Fight with another user according to the standard Arena rules."
    options=[create_option(
                    name="target",
                    description="Please choose the user who you would like to fight with.",
                    option_type=SlashCommandOptionType.USER,
                    required=True)]

    @slash.slash(name="fight", description=description, options=options)
    async def fight(ctx, target):
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
        client.current_fights.append(FightClass(ctx.author, target, client, PLAYERHP, ctx.channel.id))
        embedVar = discord.Embed(title=(f"**{ctx.author.name}** challenges **{target.name}** to a battle!"),
                                description="The first player to lose all their health loses.", color=0x00ff00)
        embedVar.add_field(name=(
            f"**{ctx.author.name}**'s lucky number is {client.luckies[ctx.author.id]} and **{target.name}**'s is {client.luckies[target.id]}."),
            value=("Type `roll` to attack and `!quit` to stop fighting."), inline=False)
        embedVar.set_thumbnail(url=(ctx.author.avatar_url))
        await ctx.send(embed=embedVar)

        select = create_select(
            options=[# the options in your dropdown
                create_select_option("Casual Fight", value="casual", emoji={'name': 'SofiaUwU', 'id': 837785194751721532}),
                create_select_option("Official Fight", value="official", emoji={'name': 'sofiagun', 'id': 809882437508399144}),
            ],
            placeholder="Choose your fight type", 
            min_values=1,  # the minimum number of options a user must select
            max_values=1,  # the maximum number of options a user can select
        )
        await ctx.send("Please choose your fight type. You can do this at any time, and this will override whatever has been selected previously.", components=[create_actionrow(select)])  # like action row with buttons but without * in front of the variable


def setlucky():
    description="Temporarily set your lucky number."
    options=[create_option(
                    name="lucky",
                    description="Choose a number between 1 and 20.",
                    option_type=SlashCommandOptionType.INTEGER,
                    required=True)]

    @slash.slash(name="setlucky", description=description, options=options)
    async def setlucky(ctx, lucky):
        if ctx.author.id in client.luckies.keys():
            await ctx.send("Your lucky number is already set as " + str(client.luckies[ctx.author.id]))
        elif 1 <= lucky <= 20:
            client.luckies[ctx.author.id] = lucky
            await ctx.send(
                "Your lucky number has been set as " + str(client.luckies[ctx.author.id]) + " until the bot is restarted.")
        else:
            await ctx.send("Please choose a number between 1 and 20 (inclusive)")

commands = {roll, setstats, stats, fight, setlucky}

def init_slashcommands(client_import, PLAYERHP_import):
    global client, slash, PLAYERHP
    client = client_import
    slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.
    PLAYERHP = PLAYERHP_import

    for i in commands:
        i()
    print("slash commands initialized!")