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


class Idiotic:
    """These commands are simply to idiotic for me."""
    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ.get("IDIOTICAPI")
        self.client = idioticapi.Client(self.token, dev=True)
        
        
    def format_avatar(self, avatar_url):
        if avatar_url.endswith(".gif"):
            return avatar_url + "?size=2048"
        return avatar_url.replace("webp", "png")


    @commands.command()
    async def blame(self, ctx, *, text=None):
        try:
            await ctx.send(file=discord.File(await self.client.blame(str(text)), "blame.png"))
        except Exception as e:
            await ctx.send(f"An error occured. \nMore details: \n{e}")
            
            
    @commands.command()
    async def triggered(self, ctx, user: discord.Member = None):
        """T R I G Gered!!!"""
        if user is None:
            user = ctx.author
        try:
            await ctx.trigger_typing()
            av = self.format_avatar(user.avatar_url)
            await ctx.send(f"B O I! {ctx.author} just made {user.name} T R I G G E R E D!!", file=discord.File(await self.client.triggered(av), "triggered.gif"))
        except Exception as e:
            await ctx.send(f"O H S N A P! something went wrong. kthnxbai. \n{e}")
            
    @commands.command()
    async def shit(self, ctx, user: discord.Member = None):
        await ctx.trigger_typing()
        user = user if user is not None else ctx.author
        try:
            await ctx.send(f"oh deer :deer:, {user.name} got stepped on. how unfortunate.", file=discord.File(await self.client.stepped(user.avatar_url), "stepped.png"))
        except Exception as e:
            await ctx.send(f"O H S N A P! something went wrong. kthnxbai. \n{e}")        
           
    @commands.command()
    async def facepalm(self, ctx, user: discord.Member = None):
        await ctx.trigger_typing()
        user = user if user is not None else ctx.author
        try:
            await ctx.send(f"oml, {user.name} had to facepalm. smh.", file=discord.File(await self.client.facepalm(user.avatar_url), "facepalm.png"))
        except Exception as e:
            await ctx.send(f"O H S N A P! something went wrong. kthnxbai. \n{e}")

    @commands.command()
    async def insult(self, ctx, user: discord.Member = None):
        await ctx.trigger_typing()
        user = user if user is not None else ctx.author
        try:
            await ctx.send(f"aw eggplants! :eggplant:, {user.name} got insulted. how unfortunate.", file=discord.File(await self.client.waifu_insult(user.avatar_url), "waifuinsult.png"))
        except Exception as e:
            await ctx.send(f"O H S N A P! something went wrong. kthnxbai. \n{e}")
            
    
    @commands.command()
    async def batslap(self, ctx, user: discord.Member = None):
        """Tag someone to give them A TASTE OF YOUR P A L M"""
        if user is None:
            await ctx.send("Tag the user first bro")
        else:
            await ctx.trigger_typing()
            try:

                av = self.format_avatar(user.avatar_url)
                avatar = self.format_avatar(ctx.author.avatar_url)
                await ctx.send(f"OOF! **{ctx.author.name}** slapped **{user.name}!**", file=discord.File(await self.client.batslap(avatar, av), "batslap.png"))
            except Exception as e:
                await ctx.send(f"O H S N A P! something went wrong. kthnxbai. \n{e}")
    
    
def setup(bot):
    bot.add_cog(Idiotic(bot))
