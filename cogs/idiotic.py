import discord 
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import sys, traceback
import random
import datetime
import time
import idioticapi

bot.api = os.environ.get("IDIOTICAPI")

class Idiotic:
    """These commands are simply to idiotic for me."""
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def blame(self, ctx, *, text):
        """Blame someone!"""
        await ctx.send(file=discord.File(await bot.api.blame(text), "blame.png"))


def setup(bot):
    bot.add_cog(Idiotic(bot))
