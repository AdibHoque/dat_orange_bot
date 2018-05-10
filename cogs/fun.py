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
    async def kappa(self, ctx):
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
    async def ayy(self, ctx):
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
    async def lenny(self, ctx):
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
    async def banhammer(self, ctx):
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
    async def doggo(self, ctx):
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
    async def mario(self, ctx):
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
    async def megaman(self, ctx):
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
    async def salt(self, ctx):
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

    @commands.command()
    async def pikachu(self, ctx):
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

    @commands.command()
    async def feels(self, ctx):
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

    @commands.command(aliases=['hypu', 'train'])
    async def hype(self, ctx):
        '''HYPE TRAIN CHOO CHOO'''
        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
                'https://gfycat.com/HairyFloweryBarebirdbat',
                'https://i.imgur.com/PFAQSLA.gif',
                'https://abload.de/img/ezgif-32008219442iq0i.gif',
                'https://i.imgur.com/vOVwq5o.jpg',
                'https://i.imgur.com/Ki12X4j.jpg',
                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
        await ctx.send(msg)    
        
        
def setup(bot):
    bot.add_cog(Fun(bot))
