"""MAIN
Program: OpenLeague > BotUtils
Author: Feven Kitsune <email upon request>
License: GNU GENERAL PUBLIC LICENSE v3.0
"""

import discord
import logging
from discord.ext import commands
from random import randint

class BotUtils():

    """INITIALIZER
    What is first called when the class ExtensionExample() is loaded. Set's the class's client variable to the client passed by the main client.
    """

    def __init__(self, client):
        self.client = client
        
    """ROLEHOLDERS
    Returns the number of members that have a certain role.
    """
    
    @commands.command(name='roleholders', aliases=['rh','rolemem'], brief='Role Holder Count', description='Returns the number of members that have a tagged role.', usage='[@tag_role]')
    async def roleholders(self, ctx, *args):
        if len(ctx.message.role_mentions) != 1:
            await ctx.send(":negative_squared_cross_mark: Incorrect syntax! Reason: Incorrect number of ROLE MENTIONS.")
            return
        
        i=0
        for m in ctx.guild.members:
            if ctx.message.role_mentions[0] in m.roles:
                i+=1
        await ctx.send(":clipboard: That role has " + str(i) + " members.")
        return
        
    """MEMBERCOUNT
    Returns the number of members in the server.
    """
    
    @commands.command(name='membercount', aliases=['mc','memcount','mcount'], brief='Server Member Count', description='Returns the number of members in the server.', usage='<none>')
    async def membercount(self, ctx, *args):
    
        if ctx.guild:
            await ctx.send(":eyes: I see " + str(len(ctx.guild.members)) + " members in this server.")
        else:
            await ctx.send(":shrug: Just you and me. This seems to be a DM channel.")
        return

    """RANDOMINT
    Generates a random number between two arguments.
    """

    @commands.command(name='randomint', aliases=['rn','randint','rint'], brief='Random Integer Generator', description='Generate an integer from <n1> to <n2>', usage='<n1> <n2>')
    async def randomint(self, ctx, *args):
    
        # No numbers passed.
        if len(args) == 0:
            await ctx.send(":negative_squared_cross_mark: Not enough arguments!")
            return
        
        # One number passed.
        if len(args) == 1:
        
            # Checks if number is an integer.
            if not isinstance(int(args[0]), int):
                await ctx.send(":negative_squared_cross_mark: Invalid arguments!")
                return
                
            await ctx.send(":game_die: " + str(randint(0, int(args[0]))))
            return

        # Two numbers passed.
        if len(args) == 2:
        
            # Checks if both numbers are integers.
            if not isinstance(int(args[0]), int) or
            not isinstance(int(args[1]), int):
                await ctx.send(":negative_squared_cross_mark: Invalid arguments!")
                return
            
            # Ensures the first number given is smaller than the second.
            if not (int(args[0]) < int(args[1])):
                await ctx.send(":negative_squared_cross_mark: Invalid arguments!")
                return
                
            await ctx.send(":game_die: " + str(randint(int(args[0]), int(args[1]))))
            return

        # More than two numbers passed.
        else:
            await ctx.send(":negative_squared_cross_mark: Too many arguments!")
            return

"""SETUP
Called by DiscordExtensions. Loads the extension into the client.
"""

def setup(client):
    client.add_cog(BotUtils(client))