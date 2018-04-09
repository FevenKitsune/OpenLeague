"""MAIN
Program: OpenLeague > BotUtils
Author: Feven Kitsune <email upon request>
License: GNU GENERAL PUBLIC LICENSE v3.0
"""

import discord
import logging
from discord.ext import commands
from random import randint

# Extension logger (Unused currently)
ext = logging.getLogger("ext")

class BotUtils():

    """INITIALIZER
    What is first called when the class ExtensionExample() is loaded. Set's the class's client variable to the client passed by the main client.
    """

    def __init__(self, client):
        self.client = client
        
    """Test
    """

    """RANDOMINT
    Generates a random number between two arguments.
    """

    @commands.command(name='randomint', aliases=['rn','randint','rint'], brief='Random Integer Generator', description='Generate an integer from <n1> to <n2>', usage='<n1> <n2>')
    async def extension(self, ctx, *args):
        if len(args) == 0:
            await ctx.send(":negative_squared_cross_mark: Not enough arguments!")
            return
            
        elif len(args) == 1:
            if isinstance(int(args[0]), int):
                await ctx.send(":game_die: " + str(randint(0, int(args[0]))))
                return
            else:
                await ctx.send(":negative_squared_cross_mark: Invalid arguments!")
                return
                
        elif len(args) == 2:
            if isinstance(int(args[0]), int) and isinstance(int(args[1]), int):
                if int(args[0]) < int(args[1]):
                    await ctx.send(":game_die: " + str(randint(int(args[0]), int(args[1]))))
                    return
                else:
                    await ctx.send(":negative_squared_cross_mark: Invalid arguments!")
                    return
                    
            else:
                await ctx.send(":negative_squared_cross_mark: Invalid arguments!")
                return
        else:
            await ctx.send(":negative_squared_cross_mark: Too many arguments!")

"""SETUP
Called by DiscordExtensions. Loads the extension into the client.
"""
def setup(client):
    client.add_cog(BotUtils(client))