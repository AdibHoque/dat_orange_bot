import discord 
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import sys, traceback
import random
import datetime
import time

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
    @commands.cooldown(1, 5, BucketType.user)
    async def say(self, ctx, *, message: commands.clean_content()):
        '''Say something as the bot'''
        voted = await self.upvoted(ctx.author.id)
        if not voted:
            return await ctx.send(f'To use this command, you must upvote RemixBot here: https://discordbots.org/bot/{self.bot.user.id}')
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        await ctx.send(message)
        
    
    

def setup(bot):
    bot.add_cog(Fun(bot))
