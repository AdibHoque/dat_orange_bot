import discord 
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import sys
import random
import datetime

class Math:
    def __init__(self, bot):
        self.bot = bot

    usage = "`[prefix] + <number 1> <number 2>`"

    @commands.command()
    async def add(self, ctx, num: int, num2: int):
        """Do some addition"""
        if num and num2 is None:
            return await ctx.send("Usage: [prefix] + [num] [num]")
        else:
            await ctx.send(num + num2)

        
    @commands.command()
    async def mul(self, ctx, num: int, num2: int):
        """Do some multiplication"""
        if num and num2 is None:
            return await ctx.send("Usage: [prefix] * [num] [num]")
        else:
            await ctx.send(num * num2)


        
    @commands.command()
    async def sub(self, ctx, num: int, num2: int):
        """Do some subtraction"""
        if num and num2 is None:
            return await ctx.send("Usage: [prefix] - [num] [num]")
        else:
            await ctx.send(num - num2)

        
    @commands.command()
    async def div(self, ctx, num: int, num2: int):
        """Do some division"""
        if num and num2 is None:
            return await ctx.send("Usage: [prefix] / [num] [num]")
        else:
            await ctx.send(num / num2)

    @commands.command()
    async def calc(self, ctx, num1=None, sign=None, num2=None):
        '''Does some simple math for you.'''
        if num1 is None:
            await ctx.send("You are missing a number. Missing Arg: num1")
        if num2 is None:
            await ctx.send("You are missing a number. Missing Arg: num2")
        if sign is None:
            await ctx.send("Please enter a sign. +, -, x, /. Missing Arg: sign \nExample: *calc 3 + 4")
        else:
            try:
                float(num1)
                float(num2)
            except ValueError:
                return await ctx.send("Usage: [prefix] */+- [num] [num]")
            else:
                num1 = float(num1)
                num2 = float(num2)
                if sign == '+':
                    color = discord.Color(value=0x00ff00)
                    em = discord.Embed(color=color, title='Calculator')
                    em.add_field(name='Input:', value=f'{num1}+{num2}')
                    em.add_field(name='Output:', value=f'{num1 + num2}')
                    return await ctx.send(embed=em)
                if sign == '-':
                    color = discord.Color(value=0x00ff00)
                    em = discord.Embed(color=color, title='Calculator')
                    em.add_field(name='Input:', value=f'{num1}-{num2}')
                    em.add_field(name='Output:', value=f'{num1 - num2}')
                    return await ctx.send(embed=em)
                if sign == 'x':
                    color = discord.Color(value=0x00ff00)
                    em = discord.Embed(color=color, title='Calculator')
                    em.add_field(name='Input:', value=f'{num1}x{num2}')
                    em.add_field(name='Output:', value=f'{num1 * num2}')
                    return await ctx.send(embed=em)
                if sign == '/':
                    color = discord.Color(value=0x00ff00)
                    em = discord.Embed(color=color, title='Calculator')
                    em.add_field(name='Input:', value=f'{num1}+{num2}')
                    em.add_field(name='Output:', value=f'{num1 / num2}')
                    return await ctx.send(embed=em)
                else:
                    return await ctx.send("Please enter a valid sign: +, -, x, / \nExample: *calc 3 + 4")

    
def setup(bot):
    bot.add_cog(Math(bot))
