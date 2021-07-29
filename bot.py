# -------------------------------import----------------------------------#
import select
import sys

import logging
import slashcommands

# My Classes
from client import * # Main class responsible for reading messages and stuff
from fight import * # Fighter class and FightClass which handles the fights
# -----------------------------------------------------------------------#


# -------------------------------variables-------------------------------#

TOKEN = ''  # Bot token
PLAYERHP = 100  # Starting health for both players
# -----------------------------------------------------------------------#

# Logging errors
logging.basicConfig(level=logging.ERROR)


# -----------------------------Slash Commands----------------------------#
client = Client()  # MyClient()
slashcommands.init_slashcommands(client, PLAYERHP)

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
