"""MAIN
Program: OpenLeague > ExtensionExample
Author: Feven Kitsune <email upon request>
License: GNU GENERAL PUBLIC LICENSE v3.0
"""

import discord
import logging
from discord.ext import commands

class ExtensionExample():

    """INITIALIZER
    What is first called when the class ExtensionExample() is loaded. Set's the class's client variable to the client passed by the main client.
    """

    def __init__(self, client):
        self.client = client

    """EXTENSION
    An example of an extension command!
    See https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5 for a useful reference about extensions.
    """

    @commands.command(name='extension', aliases=['ext'], brief='Extension example', description='An example of a loaded extension!', usage='')
    async def extension(self, ctx, *args):
        await ctx.send(":ok_hand: Extension loaded!")

"""SETUP
Called by DiscordExtensions. Loads the extension into the client.
"""

def setup(client):
    client.add_cog(ExtensionExample(client))