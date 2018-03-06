"""MAIN
Program: OpenLeague > ExtensionExample
Author: Feven Kitsune <email upon request>
License: GNU GENERAL PUBLIC LICENSE v3.0
"""

import discord
import logging
from discord.ext import commands

# Extension logger.
ext = logging.getLogger("ext")

class ExtensionExample():
    def __init__(self,client):
        self.client = client
    
    """EXTENSION
    An example of an extension!
    See https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5 for a useful reference about extensions.
    """
    
    @commands.command(name='extension', aliases=['ext'], brief='Extension example', description='An example of a loaded extension!', usage='<none>')
    async def extension(self, ctx, *args):
        await ctx.send(":ok_hand: Extension loaded!")
        
def setup(client):
    client.add_cog(ExtensionExample(client))