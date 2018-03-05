"""MAIN
Program: OpenLeague
Author: Feven Kitsune <email upon request>
License: GNU GENERAL PUBLIC LICENSE v3.0

Author Notes:
Syntax Guide: https://www.python.org/dev/peps/pep-0008
"""

import discord # Discord.py import
from discord.ext.commands import Bot # Discord.py ext import
from discord.ext import commands # Discord.py ext import
import logging # Logging import
import platform # Platform import for version checking.

"""CONFIG
Here, you can set all of the configurations for the bot.
"""

botPrefix = '!' # Default = !

"""LOGGING
Sets the logging level for the program. This makes it easier to diagnose
problems. Discord.py will output detailed information as it runs.
"""

logging.basicConfig(level=logging.INFO)
command = logging.getLogger("command")
startup = logging.getLogger("startup") # Creates a logger for use while starting up.

"""CREATE CLIENT
Here, the client is created with the given parameters.
https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#bot
You can see more parameters there.
"""

client = Bot(description="OpenLeague, the host-it-yourself alternative to MagicLeague!", command_prefix=botPrefix, pm_help=False)

"""STARTUP
The on_ready def is the first thing called when the bot is starting up.
Here, I have put a number of logging commands to output information about the bot.
"""

@client.event
async def on_ready():
    
    startup.info("Logged in as: " + client.user.name + " (ID: " + str(client.user.id) + ")")
    startup.info("Discord.py version: " + discord.__version__)
    startup.info("Python version: " + platform.python_version())
    
"""PING
The ping command is useful to check if the bot is running.
"""

@client.command(name='ping', description='A simple ping command. Checks if the bot is running!')
async def ping(ctx, *args):
    command.info(ctx.message.author.name + " ran " + ctx.invoked_with + " (args: " + str(', '.join(args)) + ")")
    if not ctx.args:
        await ctx.send(":wave: Pong!")
    else:
        await ctx.send(":wave: " + str(' '.join(args)))
    
"""RUN
To run the bot, insert your API key below.
"""

client.run("KEY")