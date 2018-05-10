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
    async def avatar(self, ctx, user : discord.Member):
        """Look at the avatar of a user"""
        embed = discord.Embed(title="Avatar of : " + user.name, url=user.avatar_url, description="[The avatar({})".format(user.avatar_url))
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def kappa(message, client):
        """Generates a Kappa face."""
        await ctx.send("""░░░░░░░░░
        ░░░░▄▀▀▀▀▀█▀▄▄▄▄░░░░
        ░░▄▀▒▓▒▓▓▒▓▒▒▓▒▓▀▄░░
        ▄▀▒▒▓▒▓▒▒▓▒▓▒▓▓▒▒▓█░
        █▓▒▓▒▓▒▓▓▓░░░░░░▓▓█░
        █▓▓▓▓▓▒▓▒░░░░░░░░▓█░
        ▓▓▓▓▓▒░░░░░░░░░░░░█░
        ▓▓▓▓░░░░▄▄▄▄░░░▄█▄▀░
        ░▀▄▓░░▒▀▓▓▒▒░░█▓▒▒░░
        ▀▄░░░░░░░░░░░░▀▄▒▒█░
        ░▀░▀░░░░░▒▒▀▄▄▒▀▒▒█░
        ░░▀░░░░░░▒▄▄▒▄▄▄▒▒█░
         ░░░▀▄▄▒▒░░░░▀▀▒▒▄▀░░
        ░░░░░▀█▄▒▒░░░░▒▄▀░░░
        ░░░░░░░░▀▀█▄▄▄▄▀""")

    @commands.command()
    async def ayy(message, client):
        """AYY LMAO"""
        await ctx.send("""░░░░█▒▒▄▀▀▀▀▀▄▄▒▒▒▒▒▒▒▒▒▄▄▀▀▀▀▀▀▄
        ░░▄▀▒▒▒▄█████▄▒█▒▒▒▒▒▒▒█▒▄█████▄▒█
        ░█▒▒▒▒▐██▄████▌▒█▒▒▒▒▒█▒▐██▄████▌▒█
        ▀▒▒▒▒▒▒▀█████▀▒▒█▒░▄▒▄█▒▒▀█████▀▒▒▒█
        ▒▒▐▒▒▒░░░░▒▒▒▒▒█▒░▒▒▀▒▒█▒▒▒▒▒▒▒▒▒▒▒▒█
        ▒▌▒▒▒░░░▒▒▒▒▒▄▀▒░▒▄█▄█▄▒▀▄▒▒▒▒▒▒▒▒▒▒▒▌
        ▒▌▒▒▒▒░▒▒▒▒▒▒▀▄▒▒█▌▌▌▌▌█▄▀▒▒▒▒▒▒▒▒▒▒▒▐
        ▒▐▒▒▒▒▒▒▒▒▒▒▒▒▒▌▒▒▀███▀▒▌▒▒▒▒▒▒▒▒▒▒▒▒▌
        ▀▀▄▒▒▒▒▒▒▒▒▒▒▒▌▒▒▒▒▒▒▒▒▒▐▒▒▒▒▒▒▒▒▒▒▒█
        ▀▄▒▀▄▒▒▒▒▒▒▒▒▐▒▒▒▒▒▒▒▒▒▄▄▄▄▒▒▒▒▒▒▄▄▀
        ▒▒▀▄▒▀▄▀▀▀▄▀▀▀▀▄▄▄▄▄▄▄▀░░░░▀▀▀▀▀▀
        ▒▒▒▒▀▄▐▒▒▒▒▒▒▒▒▒▒▒▒▒▐
        ░▄▄▄░░▄░░▄░▄░░▄░░▄░░░░▄▄░▄▄░░░▄▄▄░░░▄▄▄
        █▄▄▄█░█▄▄█░█▄▄█░░█░░░█░░█░░█░█▄▄▄█░█░░░█
        █░░░█░░█░░░░█░░░░█░░░█░░█░░█░█░░░█░█░░░█
        ▀░░░▀░░▀░░░░▀░░░░▀▀▀░░░░░░░░░▀░░░▀░▀▄▄▄▀﻿""")

    @commands.command()
    async def lenny(message, client):
        """Generate a lenny face"""
        await ctx.send("""───█───▄▀█▀▀█▀▄▄───▐█──────▄▀█▀▀█▀▄▄
    ──█───▀─▐▌──▐▌─▀▀──▐█─────▀─▐▌──▐▌─█▀
    ─▐▌──────▀▄▄▀──────▐█▄▄──────▀▄▄▀──▐▌
    ─█────────────────────▀█────────────█
    ▐█─────────────────────█▌───────────█
    ▐█─────────────────────█▌───────────█
    ─█───────────────█▄───▄█────────────█
    ─▐▌───────────────▀███▀────────────▐▌
    ──█──────────▀▄───────────▄▀───────█
    ───█───────────▀▄▄▄▄▄▄▄▄▄▀────────█""")

    @commands.command()
    async def banHammer(message, client):
        """BAN HAMMER"""
        await ctx.send("""░░░░░░░░░░░░
     ▄████▄░░░░░░░░░░░░░░░░░░░░
    ██████▄░░░░░░▄▄▄░░░░░░░░░░
    ░███▀▀▀▄▄▄▀▀▀░░░░░░░░░░░░░
    ░░░▄▀▀▀▄░░░█▀▀▄░▄▀▀▄░█▄░█░
    ░░░▄▄████░░█▀▀▄░█▄▄█░█▀▄█░
    ░░░░██████░█▄▄▀░█░░█░█░▀█░
    ░░░░░▀▀▀▀░░░░░░░░░░░░░░░░░""")

        
    @commands.command()
    async def doggo(message, client):
        """pretty pupper"""
        await ctx.send("""---------------------------
    ┈┈┈┈╱▏┈┈┈┈┈╱▔▔▔▔╲┈┈┈┈┈
    ┈┈┈┈▏▏┈┈┈┈┈▏╲▕▋▕▋▏┈┈┈┈
    ┈┈┈┈╲╲┈┈┈┈┈▏┈▏┈▔▔▔▆┈┈┈
    ┈┈┈┈┈╲▔▔▔▔▔╲╱┈╰┳┳┳╯┈┈┈
    ┈┈╱╲╱╲▏┈┈┈┈┈┈▕▔╰━╯┈┈┈┈
    ┈┈▔╲╲╱╱▔╱▔▔╲╲╲╲┈┈┈┈┈┈┈
    ┈┈┈┈╲╱╲╱┈┈┈┈╲╲▂╲▂┈┈┈┈┈
    ┈┈┈┈┈┈┈┈┈┈┈┈┈╲╱╲╱┈┈┈┈┈""")

    
    @commands.command()
    async def hitler(message, client):
        """HAIL HITLER"""
        await ctx.send("""░░░░░░░░░░░░░░░░░░
    ░░░░▓▓▀▀██████▓▄▒▒░░░
    ░░░▀░░░░░░▀▀▀████▄▒░░░
    ░░▌░░░░░░░░░░░▀███▓▒░░
    ░▌░░░░░▄▄▄░░░░░░▐█▓▒░░░
    ░▄▓▀█▌░▀██▀▒▄░░░▐▓▓▓▒░
    ░█▌░░░░░▀▒░░░▀░░░▐▓▒▒░░
    ░▌▀▒▄▄░░░░░░░░░░░░░▄▒░░
    ░▒▄█████▌▒▒░░░░░░░▒▌▒░
    ░░▓█████▄▒░▒▒▒░░░░░▐░
    ░░▒▀▓▒░░░░░░░▒▒░▒▒▒▄░
    ░░▓▒▒▒░░░░░░▒▒▒▒▒░▓░░
    ░░████▄▄▄▄▓▓▓▒▒░░▐░░
    ░░░▀██████▓▒▒▒▒▒░▐░""")

    
    @commands.command()
    async def mario(message, client):
        """IT'S-A ME-A MARIO!"""
        await ctx.send("""▒▒▒▒▒▒▒▒▒▄▄▄▄▒▄▄▄▒▒▒
    ▒▒▒▒▒▒▄▀▀▓▓▓▀█░░░█▒▒
    ▒▒▒▒▄▀▓▓▄██████▄░█▒▒
    ▒▒▒▄█▄█▀░░▄░▄░█▀▀▄▒▒
    ▒▒▄▀░██▄░░▀░▀░▀▄▓█▒▒
    ▒▒▀▄░░▀░▄█▄▄░░▄█▄▀▒▒
    ▒▒▒▒▀█▄▄░░▀▀▀█▀▓█▒▒▒
    ▒▒▒▄▀▓▓▓▀██▀▀█▄▀▒▒▒▒
    ▒▒█▓▓▄▀▀▀▄█▄▓▓▀█▒▒▒▒
    ▒▒▀▄█░░░░░█▀▀▄▄▀█▒▒▒
    ▒▒▒▄▀▀▄▄▄██▄▄█▀▓▓█▒▒
    ▒▒█▀▓█████████▓▓▓█▒▒
    ▒▒█▓▓██▀▀▀▒▒▒▀▄▄█▀▒▒
    ▒▒▒▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒""")

    
    @commands.command()
    async def megaman(message, client):
        """megaman"""
        await ctx.send("""░░░░░░░░░░▄▄█▀▀▄░░░░
    ░░░░░░░░▄█████▄▄█▄░░░░
    ░░░░░▄▄▄▀██████▄▄██░░░░
    ░░▄██░░█░█▀░░▄▄▀█░█░░░▄▄▄▄
    ▄█████░░██░░░▀▀░▀░█▀▀██▀▀▀█▀▄
    █████░█░░▀█░▀▀▀▀▄▀░░░███████▀
    ░▀▀█▄░██▄▄░▀▀▀▀█▀▀▀▀▀░▀▀▀▀
    ░▄████████▀▀▀▄▀░░░░
    ██████░▀▀█▄░░░█▄░░░░
    ░▀▀▀▀█▄▄▀░██████▄░░░░
    ░░░░░░░░░█████████░░░░""")
    
    
    @commands.command()
    async def salt(message, client):
        """Feelin' salty?"""
        await ctx.send("""▒▒▒▒▒▒▄▄██████▄
    ▒▒▒▒▒▒▒▒▒▒▄▄████████████▄
    ▒▒▒▒▒▒▄▄██████████████████
    ▒▒▒▄████▀▀▀██▀██▌███▀▀▀████
    ▒▒▐▀████▌▀██▌▀▐█▌████▌█████▌
    ▒▒█▒▒▀██▀▀▐█▐█▌█▌▀▀██▌██████
    ▒▒█▒▒▒▒████████████████████▌
    ▒▒▒▌▒▒▒▒█████░░░░░░░██████▀
    ▒▒▒▀▄▓▓▓▒███░░░░░░█████▀▀
    ▒▒▒▒▀░▓▓▒▐█████████▀▀▒
    ▒▒▒▒▒░░▒▒▐█████▀▀▒▒▒▒▒▒
    ▒▒░░░░░▀▀▀▀▀▀▒▒▒▒▒▒▒▒▒
    ▒▒▒░░░░░░░░▒▒
""")

    async def pikachu(message, client):
        """PIKACHU!"""
        await ctx.send("""░░░░█░▀▄░░░░░░░░░░▄▄███▀
    ░░░░█░░░▀▄░▄▄▄▄▄░▄▀░░░█▀
    ░░░░░▀▄░░░▀░░░░░▀░░░▄▀
    ░░░░░░░▌░▄▄░░░▄▄░▐▀▀
    ░░░░░░▐░░█▄░░░▄█░░▌▄▄▀▀▀▀█
    ░░░░░░▌▄▄▀▀░▄░▀▀▄▄▐░░░░░░█
    ░░░▄▀▀▐▀▀░░░░░░░▀▀▌▄▄▄░░░█
    ░░░█░░░▀▄░░░░░░░▄▀░░░░█▀▀▀
    ░░░░▀▄░░▀░░▀▀▀░░▀░░░▄█▀
    """)

    async def feels(message, client):
        """I ~~caused~~ feel your pain"""
        await ctx.send("""───────▄▀▀▀▀▀▀▀▀▀▀▄▄
    ────▄▀▀░░░░░░░░░░░░░▀▄
    ──▄▀░░░░░░░░░░░░░░░░░░▀▄
    ──█░░░░░░░░░░░░░░░░░░░░░▀▄
    ─▐▌░░░░░░░░▄▄▄▄▄▄▄░░░░░░░▐▌
    ─█░░░░░░░░░░░▄▄▄▄░░▀▀▀▀▀░░█
    ▐▌░░░░░░░▀▀▀▀░░░░░▀▀▀▀▀░░░▐▌
    █░░░░░░░░░▄▄▀▀▀▀▀░░░░▀▀▀▀▄░█
    █░░░░░░░░░░░░░░░░▀░░░▐░░░░░▐▌
    ▐▌░░░░░░░░░▐▀▀██▄░░░░░░▄▄▄░▐▌
    ─█░░░░░░░░░░░▀▀▀░░░░░░▀▀██░░█
    ─▐▌░░░░▄░░░░░░░░░░░░░▌░░░░░░█
    ──▐▌░░▐░░░░░░░░░░░░░░▀▄░░░░░█
    ───█░░░▌░░░░░░░░▐▀░░░░▄▀░░░▐▌
    ───▐▌░░▀▄░░░░░░░░▀░▀░▀▀░░░▄▀
    ───▐▌░░▐▀▄░░░░░░░░░░░░░░░░█
    ───▐▌░░░▌░▀▄░░░░▀▀▀▀▀▀░░░█
    ───█░░░▀░░░░▀▄░░░░░░░░░░▄▀
    ──▐▌░░░░░░░░░░▀▄░░░░░░▄▀
    ─▄▀░░░▄▀░░░░░░░░▀▀▀▀█▀
    ▀░░░▄▀░░░░░░░░░░▀░░░▀▀▀▀▄▄▄▄▄""")

def setup(bot):
    bot.add_cog(Fun(bot))
