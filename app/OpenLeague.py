"""MAIN
Program: OpenLeague
Author: Feven Kitsune <email upon request>
License: GNU GENERAL PUBLIC LICENSE v3.0

Author Notes:
Syntax Guide: https://www.python.org/dev/peps/pep-0008
"""

import discord # Discord.py import
from discord.utils import find #Discord.py find utility
from discord.ext.commands import Bot # Discord.py ext import
from discord.ext import commands # Discord.py ext import
import logging # Logging import
import platform # Platform import for version checking.

"""CONFIG
Here, you can set all of the configurations for the bot.
"""

# Prefix used for commands
botPrefix = '!' # Default = !

# A list of ID's for roles. Format: ['111111111111111111', '222222222222222222'] or ['111111111111111111']
server = [] # Only assign one server ID.
owner = []
staff = []
team_owner = []
team_staff = []
free = []

# Variables used to store role objects. Do not edit.
F_server = []
F_owner = []
F_staff = []
F_team_owner = []
F_team_staff = []
F_free = []


"""LOGGING
Sets the logging level for the program. This makes it easier to diagnose
problems. Discord.py will output detailed information as it runs.
"""

logging.basicConfig(level=logging.INFO)
command = logging.getLogger("command") # The command logger is used while the bot is running.
startup = logging.getLogger("startup") # The startup logger is used during startup.

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

    # Global variables to assign server variables.
    global F_server
    global F_owner
    global F_staff
    global F_team_owner
    global F_team_staff
    global F_free
    
    # Startup information
    startup.info("Logged in as: " + client.user.name + " (ID: " + str(client.user.id) + ")")
    startup.info("Discord.py version: " + discord.__version__)
    startup.info("Python version: " + platform.python_version())
    
    # Check to make sure there isn't more than one server in config.
    if len(server) > 1:
        startup.warn("More than one server provided in config! Please edit the config.")
        await client.close()
        
    # Check to make sure there is a server in config.
    if len(server) < 1:
        startup.warn("No server provided in config! Please edit the config.")
        await client.close()
    
    # Find server and assign it to F_server.
    F_server = find(lambda a: str(a.id) == server[0], client.guilds)
    
    # If the server is not found, throw an error.
    if not F_server:
        startup.warn("Was unable to find " + str(server[0]) + " as a server! Please check your config.")
        await client.close()
    
    # Find owner roles and assign them to F_owner
    for id in owner:
        find_role = find(lambda b: str(b.id) == id, F_server.roles)
        if find_role:
            startup.info("Found owner role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_owner.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
            
    # Find staff roles and assign them to F_staff
    for id in staff:
        find_role = find(lambda b: str(b.id) == id, F_server.roles)
        if find_role:
            startup.info("Found staff role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_staff.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
            
    # Find team_owner roles and assign them to F_team_owner
    for id in team_owner:
        find_role = find(lambda b: str(b.id) == id, F_server.roles)
        if find_role:
            startup.info("Found team_owner role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_team_owner.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
    
    # Find team_staff roles and assign them to F_team_staff
    for id in team_staff:
        find_role = find(lambda b: str(b.id) == id, F_server.roles)
        if find_role:
            startup.info("Found team_staff role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_team_staff.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
    
    # Find free roles and assign them to F_free
    for id in free:
        find_role = find(lambda b: str(b.id) == id, F_server.roles)
        if find_role:
            startup.info("Found free role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_free.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
    
"""PING
The ping command is useful to check if the bot is running.
"""

@client.command(name='ping', description='A simple ping command. Checks if the bot is running!')
async def ping(ctx, *args):

    command.info(ctx.message.author.name + " ran " + ctx.invoked_with + " (args: " + str(', '.join(args)) + ")")
    
    if not args:
        await ctx.send(":wave: Pong!")
    else:
        await ctx.send(":wave: " + str(' '.join(args)))
        
"""GETID
The getid command will return the ID of a tagged member, role, or channel.
"""

@client.command(name='getid', description='Returns the ID of a member, role, or channel.')
async def getid(ctx, *args):

    command.info(ctx.message.author.name + " ran " + ctx.invoked_with + " (args: " + str(', '.join(args)) + ")")
    
    if not args:
        await ctx.send(":negative_squared_cross_mark: Nothing tagged.")
    else:
        pl = ""
        for member in ctx.message.mentions:
            pl = pl + ":bust_in_silhouette: " + member.name + ": " + str(member.id) + "\n"
        for channel in ctx.message.channel_mentions:
            pl = pl + ":page_facing_up: " + channel.name + ": " + str(channel.id) + "\n"
        for role in ctx.message.role_mentions:
            pl = pl + ":name_badge: " +  role.name + ": " + str(role.id) + "\n"
        await ctx.send(pl)
    
"""RUN
To run the bot, insert your API key below.
"""

client.run("KEY")