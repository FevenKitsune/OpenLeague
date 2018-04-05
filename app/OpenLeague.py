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
import json # Settings loader
import os, sys # Execution location

"""CONFIG
Here, the JSON is loaded, and put into their respective variables.
"""

with open(os.path.join(sys.path[0], 'botfile.json')) as json_data:
    j = json.load(json_data)
    print(j)
    print(j['owner'][0])

# Extensions are placed here.
startup_extensions = j['extensions']

# Enable or disable various functions of the bot
transactions_toggle = j['transaction_toggle']
promotions_toggle = j['promotion_toggle']

# Transaction channel settings
transactionChannel_toggle = j['transaction_channel_settings'][0] # Can equal True or False.
transactionChannel = j['transaction_channel_settings'][1]

# Promotion channel settings
promotionChannel_toggle = j['promotion_channel_settings'][0] # Can equal True or False.
promotionChannel = j['transaction_channel_settings'][1]

# A list of ID's for roles. Format: [111111111111111111, 222222222222222222] or [111111111111111111]
server = j['server']
owner = j['owner']
staff = j['staff']
team_owner = j['team_owner']
team_staff = j['team_staff']
free = j['free']

# Sign and Release Messages
SIGN_MESSAGE = j['sign_message']
RELEASE_MESSAGE = j['release_message']

# Other constants
SOURCE_CODE_URL = "https://github.com/FevenKitsune/OpenLeague"
BOT_DESCRIPTION = j['description']
BOT_PREFIX = j['prefix'] # Default: !
BOT_KEY = j['key']

# F_ROLE/SERVER Object Cache
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

client = Bot(description=BOT_DESCRIPTION, command_prefix=BOT_PREFIX, pm_help=False)

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
    F_server = find(lambda a: a.id == server[0], client.guilds)
    
    # If the server is not found, throw an error.
    if not F_server:
        startup.warn("Was unable to find " + str(server[0]) + " as a server! Please check your config.")
        await client.close()
    
    # Find owner roles and assign them to F_owner
    for id in owner:
        find_role = find(lambda b: b.id == id, F_server.roles)
        if find_role:
            startup.info("Found owner role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_owner.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
            
    # Find staff roles and assign them to F_staff
    for id in staff:
        find_role = find(lambda b: b.id == id, F_server.roles)
        if find_role:
            startup.info("Found staff role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_staff.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
            
    # Find team_owner roles and assign them to F_team_owner
    for id in team_owner:
        find_role = find(lambda b: b.id == id, F_server.roles)
        if find_role:
            startup.info("Found team_owner role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_team_owner.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
    
    # Find team_staff roles and assign them to F_team_staff
    for id in team_staff:
        find_role = find(lambda b: b.id == id, F_server.roles)
        if find_role:
            startup.info("Found team_staff role: " + find_role.name +" (ID: " + str(find_role.id) + ")")
            F_team_staff.append(find_role)
        else:
            startup.warn("Was unable to find " + str(id) + " on the given server! Please check your config.")
            await client.close()
    
    # Find free roles and assign them to F_free
    for id in free:
        find_role = find(lambda b: b.id == id, F_server.roles)
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
            find_channel = find(lambda b: b.id == transactionChannel[0], F_server.channels)
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
            find_channel = find(lambda b: b.id == promotionChannel[0], F_server.channels)
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

# ARGUMENTS: User, Role
# USE: Sets the given User to the Role, and verifies that the user has the role.
async def set_role(u, r):
    while r not in u.roles:
        await u.add_roles(r)

# ARGUMENTS: User, Role
# USE: Removes the given Role from the User and verifies the role was removed.
async def rm_role(u, r):
    while r in u.roles:
        await u.remove_roles(r)

# ARGUMENTS: User, Role
# USE: Checks if the given User has the given Role and returns True.
async def has_role(u, r):
    if r in u.roles: return True
    else: return False

# ARGUMENTS: User, Server
# USE: Gives all roles in free[] to given User. Server pass is required so the bot knows what server to search.
async def set_free(u, s):
    for r in F_free:
        await set_role(u, r)

# ARGUMENTS: User
# USE: Gets all roles from User, and compares them to values in the free[] list. If the values match, remove the role and move on.
async def rm_free(u):
    for r in u.roles:
        if r in F_free:
            await rm_role(u, r)

# ARGUMENTS: User
# USE: Checks if given User has any roles that match any of the roles in free[].
async def is_free(u):
    return [i for i in [role for role in u.roles] if i in F_free]

# ARGUMENTS: User
# USE: Checks if given User has any roles that match any of the roles in owner[].
async def is_owner(u):
    return [i for i in [role for role in u.roles] if i in F_owner]

# ARGUMENTS: User
# USE: Checks if given User has any roles that match any of the roles in staff[].
async def is_staff(u):
    return [i for i in [role for role in u.roles] if i in F_staff]

# ARGUMENTS: User, Role
# USE: Checks if given User has any roles that match any of the roles in team_owner[].
async def is_team_owner(u, r):
    return [i for i in [role for role in u.roles] if i in F_team_owner]

# ARGUMENTS: User, Role
# USE: Checks if given User has any roles that match any of the roles in team_staff[].
async def is_team_staff(u, r):
    return [i for i in [role for role in u.roles] if i in F_team_staff]
    
# ARGUMENTS: Context
# USE: Posts a sign message to the given message context when a user is signed.
async def sign_message(ctx):
    print("filler")

# ARGUMENTS: Context
# USE: Posts a release message to the given message context when a user is released.
async def release_message(ctx):
    print("filler")
    

"""PING
The ping command is useful to check if the bot is running.
"""

@client.command(name='ping', brief='Ping the bot', description='A simple ping command. Checks if the bot is running!', usage='<string>')
async def ping(ctx, *args):

    command.info(ctx.message.author.name + " ran " + ctx.invoked_with + " (args: " + str(', '.join(args)) + ")")
    
    if not args:
        await ctx.send(":wave: Pong!")
    else:
        await ctx.send(":wave: " + str(' '.join(args)))
        
"""GETID
The getid command will return the ID of a tagged member, role, or channel.
"""

@client.command(name='getid', aliases=['gid','id'], brief='Search tagged objects', description='Returns the ID of a member, role, or channel.', usage='[@tag_player]/[@tag_team]/[@tag_channel]')
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

    staff_role = None
    team_role = None
    
    # CHECKS
    
    if (len(ctx.message.mentions) != 1):
        await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of USER MENTIONS.")
        return
        
    if (len(ctx.message.role_mentions) != 2):
        await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of ROLE MENTIONS.")
        return

    if ((ctx.message.role_mentions[0] in F_team_staff) and not (ctx.message.role_mentions[1] in F_team_staff)):
        staff_role = ctx.message.role_mentions[0]
    elif ((ctx.message.role_mentions[1] in F_team_staff) and not (ctx.message.role_mentions[0] in F_team_staff)):
        staff_role = ctx.message.role_mentions[1]
    else:
        await ctx.send(":negative_squared_cross_mark: Neither of the roles or both of the roles you mentioned are team staff roles!")
        return
    
    if not (await is_owner(ctx.message.author) or 
    await is_staff(ctx.message.author) or 
    await is_team_owner(ctx.message.author, team_role)):
        await ctx.send(":negative_squared_cross_mark: You do not have permission to do that.")
        return
    
    if (await is_team_staff(ctx.message.mentions[0], team_role)):
        await ctx.send(":negative_squared_cross_mark: The mentioned user is currently team staff.")
        return
        
    if (await is_team_owner(ctx.message.mentions[0], team_role)):
        await ctx.send(":negative_squared_cross_mark: The mentioned user is currently team owner.")
        return

    await set_role(ctx.message.mentions[0], staff_role)
    await ctx.send(":star2: " + ctx.message.mentions[0].mention + " was promoted to " + staff_role.mention)

"""DEMOTE
Filler
"""

@client.command(name='demote', aliases=['d'], brief='Demote user', description='Removes all team_staff ranks from a tagged player.', usage='[@tag_player] [@tag_team] [@tag_role]')
async def demote(ctx, *args):

    staff_role = None
    team_role = None

    # CHECKS
    
    if (len(ctx.message.mentions) != 1):
        await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of USER MENTIONS.")
        return
        
    if (len(ctx.message.role_mentions) != 2):
        await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of ROLE MENTIONS.")
        return
    
    if ((ctx.message.role_mentions[0] in F_team_staff) and not (ctx.message.role_mentions[1] in F_team_staff)):
        staff_role = ctx.message.role_mentions[0]
    elif ((ctx.message.role_mentions[1] in F_team_staff) and not (ctx.message.role_mentions[0] in F_team_staff)):
        staff_role = ctx.message.role_mentions[1]
    else:
        await ctx.send(":negative_squared_cross_mark: Neither of the roles or both of the roles you mentioned are team staff roles!")
        return
    
    if not (await is_owner(ctx.message.author) or 
    await is_staff(ctx.message.author) or 
    await is_team_owner(ctx.message.author, team_role)):
        await ctx.send(":negative_squared_cross_mark: You do not have permission to do that.")
        return
    
    if not (await is_team_staff(ctx.message.mentions[0], team_role)):
        await ctx.send(":negative_squared_cross_mark: The mentioned user is not currently team staff.")
        return
        
    if not (await has_role(ctx.message.mentions[0], staff_role)):
        await ctx.send(":negative_squared_cross_mark: The mentioned user does not have the mentioned team staff role.")
        return
        
    await rm_role(ctx.message.mentions[0], staff_role)
    await ctx.send(":arrow_heading_down: " + ctx.message.mentions[0].mention + " was demoted from " + staff_role.mention)
    

"""SIGN
filler
"""

@client.command(name='sign', aliases=['s'], brief='Sign user', description='Sign a player to a tagged team.', usage='[@tag_player] [@tag_team]')
async def sign(ctx, *args):

    # CHECKS
    
    if (len(ctx.message.mentions) != 1):
        await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of USER MENTIONS.")
        return
        
    if (len(ctx.message.role_mentions) != 1):
        await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of ROLE MENTIONS.")
        return

    if not (await is_owner(ctx.message.author) or 
    await is_staff(ctx.message.author) or 
    await is_team_owner(ctx.message.author, ctx.message.role_mentions[0]) or 
    await is_team_staff(ctx.message.author, ctx.message.role_mentions[0])):
        await ctx.send(":negative_squared_cross_mark: You do not have permission to do that.")
        return
        
    if not (await is_free(ctx.message.mentions[0])):
        await ctx.send(":negative_squared_cross_mark: The mentioned user is not a free agent.")
        return
        
    await rm_free(ctx.message.mentions[0])
    await set_role(ctx.message.mentions[0], ctx.message.role_mentions[0])
    await ctx.send(":pen_fountain: " + ctx.message.mentions[0].mention + " was signed to " + ctx.message.role_mentions[0].mention)

"""RELEASE
Filler
"""

@client.command(name='release', aliases=['r'], brief='Release user', description='Release a player from a tagged team.', usage='[@tag_player] [@tag_team]')
async def release(ctx, *args):

    # CHECKS

    if (len(ctx.message.mentions) != 1):
        await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of USER MENTIONS.")
        return
        
    if (len(ctx.message.role_mentions) != 1):
        await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of ROLE MENTIONS.")
        return
        
    if not (await is_owner(ctx.message.author) or 
    await is_staff(ctx.message.author) or 
    await is_team_owner(ctx.message.author, ctx.message.role_mentions[0]) or 
    await is_team_staff(ctx.message.author, ctx.message.role_mentions[0])):
        await ctx.send(":negative_squared_cross_mark: You do not have permission to do that.")
        return
        
    if not (await has_role(ctx.message.mentions[0], ctx.message.role_mentions[0])):
        await ctx.send(":negative_squared_cross_mark: The mentioned user is not on that team.")
        return
        
    if (await is_team_owner(ctx.message.mentions[0], ctx.message.role_mentions[0]) or 
    await is_team_staff(ctx.message.mentions[0], ctx.message.role_mentions[0])):
        await ctx.send(":negative_squared_cross_mark: The mentioned user is currently a staff member. Demote them before releasing them.")
        return
        
    await rm_role(ctx.message.mentions[0], ctx.message.role_mentions[0])
    await set_free(ctx.message.mentions[0], ctx.message.guild)
    await ctx.send(":exclamation: " + ctx.message.mentions[0].mention + " was released from " + ctx.message.role_mentions[0].mention)

"""MSGROLE
Unknown use yet.
"""

@client.command(name='msgrole', aliases=['mr'], brief='Staff command. Message role.', description='Staff only. Message all members of a tagged role.', usage='[@tag_role] [string]')
async def msgrole(ctx, *args):
    print("filler")

"""SOURCE
Posts a URL to the bot's sourcecode.
"""

@client.command(name='source', brief='Source code', description='Get information about the bot, as well as a link to the source code.', usage='')
async def source(ctx, *args):
    await ctx.send(":computer: See the source code at <" + SOURCE_CODE_URL + ">")
    
"""RUN
To run the bot, insert your Discord Developers Token below.
"""

client.run(BOT_KEY) # Put your Discord Developers Token here!