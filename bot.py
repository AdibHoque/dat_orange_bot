import discord 
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import sys

bot = commands.Bot(command_prefix="bz.", owner_id=426060491681431562)

@bot.event
async def on_ready():
    while True:
        await bot.change_presence(activity=discord.Game(name='bz.help with my friends!'))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game('with dat banana bot'))
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Game(f'with {len(client.guilds)} servers'))

@bot.event
async def on_command_error(ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send("You lack the nessecary permissions to use this command. Please get your superior.")  
        


@bot.command(pass_context=True)
async def ping(ctx):
    embed = discord.Embed(title="Bravo Zulu! | My latency is: ", color=0x00ff00)
    embed.description = f"{bot.latency * 1000:.4f} ms"
    await ctx.send(embed=embed)

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="Not a title", description="Not a description", color = 0x00ff00)
    embed.set_footer(text="Not a footer")
    embed.set_author(name="Not an author")
    embed.add_field(name="Not a name", value = "No value", inline = False)
    await ctx.send(embed=embed)

#owner commands


@bot.command()
@commands.is_owner()
async def restart(ctx):
        msg = await ctx.send("Restarting the bot now.")
        await asyncio.sleep(1)
        await msg.edit(content="Peace! Restarting!")
        os.execv(sys.executable, ['python'] + ['\\Users\\megat\\Desktop\\bravo_zulu\\bot.py'])


@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount, description="Clears messages from the chat"):
    try:
        x = int(amount)
        if x < 2 or x > 500:
            return await ctx.send("Must be in range of 2 to 500 messages.")
        await ctx.channel.purge(limit=x)
        await ctx.send("Cleared {} messages for you. Emjoy the clear chat!", delete_after=5)
    except ValueError:
        await ctx.send("Please select a number.")
    except commands.errors.MissingPermissions:
        await ctx.send(on_command_error)
    except Exception as e:
        await ctx.send("Something went wrong. Here it is: {}".format(e))
        print(e)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member):
    try:
        await ctx.send(f"**{user.name}** has been kicked from the server.")
        await ctx.guild.kick(user)
    except discord.Forbidden:
        await ctx.send(f"Bravo Zulu lacks the permission to kick **{user.name}**.")
    except commands.errors.MissingPermissions:
        await ctx.send("You don't have the nessecary perms to do that.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member):
    try:
        await ctx.send(f'**{user.name}** is now banned from the server!')
        await ctx.guild.ban(user)
    except discord.Forbidden:
        await ctx.send(f"Bravo Zulu lacks the permission to ban **{user.name}**.")
    except commands.errors.MissingPermissions:
        await ctx.send("no perms bro")
        


    

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="Bravo Zulu invite link!", color=0xce1414)
    embed.description = "https://discordapp.com/api/oauth2/authorize?client_id=439919013766758420&permissions=305454295&scope=bot :smile: :muscle::skin-tone-2:"
    await ctx.send(embed = embed)

@bot.command()
async def support(ctx):
    embed = discord.Embed(title='Bravo Zulu Support Server', color=0xce1414)
    embed.description = "https://discord.gg/EvjMmPB"
    await ctx.send(embed=embed)


@bot.command()
async def contributors(ctx):
    embed = discord.Embed(title="Bravo Zulu Developers", color=0xce1414)
    embed.description = "Main Devs: \n Bravo Zulu#0638 \n FreeTNT#5796 \n CyRIC#0847 \n Sub Devs: \n L3NNY#4519 \n dat banana boi#1982 \n Ice#1234"
    await ctx.send(embed=embed)


@bot.command()
async def add(ctx, a, b):
    try:
        a, b = int(a), int(b)
        await ctx.send(a + b)
    except ValueError:
        await ctx.send("That is not a vaild integer. Please try again. This bot does not support decimal numbers.")

@bot.command()
async def mul(ctx, a, b):
    try:
        a, b = int(a), int(b)
        await ctx.send(a * b)
    except ValueError:
        await ctx.send("That is not a valid integer. Please try again. This bot does not support decimal numbers.")

@bot.command()
async def sub(ctx, a, b):
    try:
        a, b = int(a), int(b)
        await ctx.send(a - b)
    except ValueError:
        await ctx.send("That is not a valid integer. Please try again. This bot does not support decimal numbers.")

@bot.command()
async def div(ctx, a, b):
    try:
        a, b = int(1), int(2)
        await ctx.send(a / b)
    except ValueError:
        await ctx.send("That is not a valid integer. Please try again. This bot does not support decimal numbers.")
    

bot.run(os.environ.get('TOKEN'))
