import discord 
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import sys, traceback
import random
import datetime
import time
import requests

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)

class Fun:
    """Use these commands to have some fun!"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def poll(self, ctx, *, question):
        """To vote, use reactions!"""
        messages = [ctx.message]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100

        for i in range(20):
            messages.append(await ctx.send(f"Say poll option or {ctx.prefix}publish to publish poll."))

            try:
                entry = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                break

            messages.append(entry)

            if entry.clean_content.startswith(f"{ctx.prefix}publish"):
                break
            
            answers.append((to_emoji(i), entry.clean_content))

        try:
            await ctx.channel.delete_messages(messages)
        except:
            pass

        answer = "\n".join(f"{keycap}: {content}" for keycap, content in answers)
        actual_poll = await ctx.send(f"{ctx.author} asks: {question}\n\n{answer}")
        for emoji, _ in answers:
            await actual_poll.add_reaction(emoji)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("You are missing the question.")


        
    @commands.command()
    async def sun(self, ctx):
        '''Praise the Sun'''
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')
        
    @commands.command()
    async def countdown(self, ctx):
        '''It's the final countdown'''
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await ctx.send('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await ctx.send('https://media.giphy.com/media/jVStxzak9yk2Q/giphy.gif')
        
        
    @commands.command()
    async def randomcat(self, ctx):
        """Display a random cat"""

        r = requests.get('http://random.cat/meow.php')
        cat = str(r.json()['file'])
        embed = discord.Embed(title="Meow", description="({})".format(cat), colour=0x03C9A9)
        embed.set_thumbnail(url=cat)
        embed.set_author(name="Random.cat", url='https://random.cat/', icon_url='http://outout.tech/tuxbot/nyancat2.gif')
        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Fun(bot))
