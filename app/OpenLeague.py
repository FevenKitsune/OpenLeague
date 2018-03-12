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

# Extensions are placed here.
startup_extensions = ["ExtensionExample"]

# Prefix used for commands
botPrefix = '!' # Default = !

# Enable or disable various functions of the bot
transactions_toggle = True # Can equal True or False.
promotions_toggle = True # Can equal True or False.

# Transaction channel settings
transactionChannel_toggle = True # Can equal True or False.
transactionChannel = ['409439762689163275'] # Format: ['111111111111111111']

# Promotion channel settings
promotionChannel_toggle = True # Can equal True or False.
promotionChannel = ['409439762689163275'] # Format: ['111111111111111111']

# A list of ID's for roles. Format: ['111111111111111111', '222222222222222222'] or ['111111111111111111']
server = ['385059238231408651'] # Only assign one server ID.
owner = ['385059307110137856']
staff = ['414881926630080512']
team_owner = ['409468370191253514']
team_staff = ['409468200347238421']
free = ['385059381391392770']

# Variables used to store role objects. Do not edit.
F_server = []
F_owner = []
F_staff = []
F_team_owner = []
F_team_staff = []
F_free = []

# Variables used to store channel objects. Do not edit.
F_transactionChannel = []
F_promotionChannel = []


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
    
    global F_transactionChannel
    global F_promotionChannel
    
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
            
    # Check if transaction toggle is enabled, and find the channel.
    if transactionChannel_toggle == True:
        if len(transactionChannel) > 1:
            startup.warn("Multiple transaction channels detected. Please check your config.")
            await client.close()
        elif len(transactionChannel) < 1:
            startup.warn("transactionChannel_toggle is enabled, but no channel is given. Please check your config.")
            await client.close()
        else:
            find_channel = find(lambda b: str(b.id) == transactionChannel[0], F_server.channels)
            if find_channel:
                startup.info("Found transaction channel: " + find_channel.name + " (ID: " + str(find_channel.id) + ")")
                F_transactionChannel = find_channel
            else:
                startup.warn("Was unable to find " + str(find_channel.id) + " on the given server! Please check your config.")
                await client.close()
    
    # Check if promotion toggle is enabled, and find the channel.
    if promotionChannel_toggle == True:
        if len(promotionChannel) > 1:
            startup.warn("Multiple promotion channels detected. Please check your config.")
            await client.close()
        elif len(promotionChannel) < 1:
            startup.warn("promotionChannel_toggle is enabled, but no channel is given. Please check your config.")
            await client.close()
        else:
            find_channel = find(lambda b: str(b.id) == promotionChannel[0], F_server.channels)
            if find_channel:
                startup.info("Found promotion channel: " + find_channel.name + " (ID: " + str(find_channel.id) + ")")
                F_promotionChannel = find_channel
            else:
                startup.warn("Was unable to find " + str(find_channel.id) + " on the given server! Please check your config.")
                await client.close()
                
    # Extension loader. Loads extensions listed above.
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception:
            startup.warn("Failed to load extension: " + extension)
        else:
            startup.info("Loaded extension: " + extension)
    
"""CHECKS
Check definitions allow commands to run permission checks easily.
"""

async def set_role(u, r):

async def is_owner(u):

async def is_staff(u):

async def is_team_owner(u, r):

async def is_team_staff(u, r):

async def is_free(u):

"""
#Returns true if author is server owner
def is_serverowner(ctx):
    return [i for i in [str(role.id) for role in ctx.message.author.roles] if i in owner]
    
#Returns true if author is server staff
def is_serverstaff(ctx):
    return [i for i in [str(role.id) for role in ctx.message.author.roles] if i in staff]
    
#Returns true if author is team owner
def is_teamowner(ctx):
    if ctx.message.role_mentions[0] in ctx.message.author.roles:
        return [i for i in [str(role.id) for role in ctx.message.author.roles] if i in team_owner]
    
#Returns true if author is team staff.
def is_teamstaff(ctx):
    if ctx.message.role_mentions[0] in ctx.message.author.roles:
        return [i for i in [str(role.id) for role in ctx.message.author.roles] if i in team_staff]

#Returns true if mentioned user is a free agent.
def is_free(ctx):
    return [i for i in [str(role.id) for role in ctx.message.mentions[0].roles] if i in free]
    
#Returns true if mentioned user is team_staff or team_owner
def team_position(ctx):
    if [i for i in [str(role.id) for role in ctx.message.mentions[0].roles] if i in team_staff] or [i for i in [str(role.id) for role in ctx.message.mentions[0].roles] if i in team_owner]:
        return True
    return False
    
#Iterates and removes all free agent roles.
async def rm_free(ctx):
    for r in ctx.message.mentions[0].roles:
        if str(r.id) in free:
            while r in ctx.message.mentions[0].roles:
                await ctx.message.mentions[0].remove_roles(r)
                
#Gives mentioned user free roles.
async def set_free(ctx):
    for r in free:
        far = discord.utils.find(lambda f: f.id == int(r), ctx.message.guild.roles)
        while far not in ctx.message.mentions[0].roles:
            await ctx.message.mentions[0].add_roles(far)
                
#Signs user to the first mentioned team.
async def set_team(ctx):
    while ctx.message.role_mentions[0] not in ctx.message.mentions[0].roles:
        await ctx.message.mentions[0].add_roles(ctx.message.role_mentions[0])

#Checks if mentioned user is on mentioned team        
def on_team(ctx):
    if ctx.message.role_mentions[0] in ctx.message.mentions[0].roles:
        return True
    return False
    
#Removes tagged team from tagged user
async def rm_team(ctx):
    while ctx.message.role_mentions[0] in ctx.message.mentions[0].roles:
        await ctx.message.mentions[0].remove_roles(ctx.message.role_mentions[0])"""
        
#Posts sign message
async def sign_message(ctx):
    

#Posts release message
async def release_message(ctx):
    

"""PING
The ping command is useful to check if the bot is running.
"""

@client.command(name='ping', brief='Ping the bot', description='A simple ping command. Checks if the bot is running!')
async def ping(ctx, *args):

    command.info(ctx.message.author.name + " ran " + ctx.invoked_with + " (args: " + str(', '.join(args)) + ")")
    
    if not args:
        await ctx.send(":wave: Pong!")
    else:
        await ctx.send(":wave: " + str(' '.join(args)))
        
"""GETID
The getid command will return the ID of a tagged member, role, or channel.
"""

@client.command(name='getid', aliases=['gid','id'], brief='Search tagged objects', description='Returns the ID of a member, role, or channel.')
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
        
"""PROMOTE
Filler
"""

@client.command(name='promote', aliases=['p'], brief='Promote user', description='Gives tagged player the tagged team_staff rank.', usage='[@tag_player] [@tag_team] [@tag_role]')
async def promote(ctx, *args):
    print("filler")

"""DEMOTE
Filler
"""

@client.command(name='demote', aliases=['d'], brief='Demote user', description='Removes all team_staff ranks from a tagged player.')
async def demote(ctx, *args):
    print("filler")

"""SIGN
Filler
"""

@client.command(name='sign', aliases=['s'], brief='Sign user', description='Sign a player to a tagged team.')
async def sign(ctx, *args):
    print("sign")
    if len(ctx.message.mentions)==1 and len(ctx.message.role_mentions)==1:
        if is_serverowner(ctx) or is_serverstaff(ctx) or is_teamowner(ctx) or is_teamstaff(ctx):
            if is_free(ctx):
                await rm_free(ctx)
                await set_team(ctx)
                await ctx.send(ctx.message.mentions[0].mention + " was signed to " + ctx.message.role_mentions[0].mention)
            else:
                await ctx.send(":negative_squared_cross_mark: Sorry, that user is not a free agent.")
        else:
            await ctx.send(":negative_squared_cross_mark: Sorry, you don't have permission to do that.")
    else:
        await ctx.send(":negative_squared_cross_mark: Invalid syntax, please check formatting.")

"""RELEASE
Filler
"""

@client.command(name='release', aliases=['r'], brief='Release user', description='Release a player from a tagged team.')
async def release(ctx, *args):
    if len(ctx.message.mentions)==1 and len(ctx.message.role_mentions)==1:
        if is_serverowner(ctx) or is_serverstaff(ctx) or is_teamowner(ctx) or is_teamstaff(ctx):
            if on_team(ctx):
                if not team_position(ctx):
                    await rm_team(ctx)
                    await set_free(ctx)
                    await ctx.send(ctx.message.mentions[0].mention + " was released from " + ctx.message.role_mentions[0].mention)
                else:
                    await ctx.send(":negative_squared_cross_mark: Sorry, that user is still staff! Please demote them first.")
            else:
                await ctx.send(":negative_squared_cross_mark: Sorry, that user is not on that team.")
        else:
            await ctx.send(":negative_squared_cross_mark: Sorry, you don't have permission to do that.")
    else:
        await ctx.send(":negative_squared_cross_mark: Invalid syntax, please check formatting.")

"""MSGROLE
Filler
"""

@client.command(name='msgrole', aliases=['mr'], brief='Staff command. Message role.', description='Staff only. Message all members of a tagged role.')
async def msgrole(ctx, *args):
    print("filler")

"""SOURCE
Link to source code
"""

@client.command(name='source', brief='Source code', description='Get information about the bot, as well as a link to the source code.')
async def source(ctx, *args):
    print("filler")
    
"""RUN
To run the bot, insert your Discord Developers Token below.
"""

client.run("KEY") # Put your Discord Developers Token here!