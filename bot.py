import discord 
from discord.ext import commands
import asyncio
import os
import json
import traceback
from motor.motor_asyncio import AsyncIOMotorClient
import sys
import textwrap
import io
from contextlib import redirect_stdout
import random
import inspect

bravo_db = AsyncIOMotorClient(os.environ.get("MONGODB"))

async def get_prefix(bot, message):
    l = await bravo_db.bravo.prefix.find_one({"id": str(message.guild.id)})
    if l is None:
        return "o."
    pre = l.get('prefix', "o.")
    return pre

bot = commands.Bot(command_prefix=get_prefix, owner_id=426060491681431562)
bot.db = bravo_db

bot._last_result = None
bot.remove_command("help")

def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

async def save_prefix(prefix, guildID, ctx):
    await bravo_db.bravo.prefix.update_one({"id": str(ctx.guild.id)}, {"$set": {"prefix": prefix}}, upsert=True)

bot.load_extension("cogs.Errorhandler")
bot.load_extension("cogs.Help")
bot.load_extension("cogs.mod")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.pubg")
bot.load_extension("cogs.math")
bot.load_extension("cogs.idiotic")
bot.load_extension("cogs.info")
bot.load_extension("cogs.tags")
    
if 'TOKEN' in os.environ:
    heroku = True
    TOKEN = os.environ['TOKEN']
    
def dev_check(id):
    with open('data/devs.json') as f:
        devs = json.load(f)
        if id in devs:
            return True
        return False
    
    
@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(441408391676559361)
    embed = discord.Embed(title='New Server!', description=f'Server Name: {guild.name} | Server Num {len(bot.guilds)}', color=discord.Color.green())
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"Server ID: {guild.id}")
    embed.set_author(name=f"Owner: {guild.owner} | ID: {guild.owner.id}", icon_url=guild.owner.avatar_url)
    await channel.send(embed=embed)


@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(441408391676559361)
    embed = discord.Embed(title='Removed from Server', description=f'Server Name: {guild.name} | Server Num {len(bot.guilds)}', color=discord.Color.red())
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"Server ID: {guild.id}")
    embed.set_author(name=f"Owner: {guild.owner} | ID: {guild.owner.id}", icon_url=guild.owner.avatar_url)
    await channel.send(embed=embed)
    
@bot.event
async def on_ready():
    print("----------------")
    print("Logged in as:")
    print("Name : {}".format(bot.user.name))
    print("ID : {}".format(bot.user.id))
    print("Py Lib Version: %s"%discord.__version__)
    print("----------------")
    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def prefix(ctx, prefix=None):
    """Change Prefix of the server"""
    guildID = str(ctx.guild.id)
    if not prefix:
        return await ctx.send('Please provide a prefix for this command to work')
    try:
        await save_prefix(prefix, guildID, ctx)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')
    except Exception as e:
        await ctx.send(f'Something went wrong\nError Log: `str({e})`')

@bot.event
async def on_ready():
    while True:
        await bot.change_presence(activity=discord.Game(name='o.help!'))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(f'with {len(bot.guilds)} servers'))
        await asyncio.sleep(10)
        

        
@bot.event
async def on_message(msg):
    """Ignores the message of bots."""
    if not msg.author.bot:
        await bot.process_commands(msg)

@bot.command(pass_context=True)
async def ping(ctx):
    embed = discord.Embed(title="dat orange bot | My latency is: ", color=0x00ff00)
    embed.description = f"{bot.latency * 1000:.4f} ms \n WoAh THATS ~~hella~~ fast!!"
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
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


        
        
@bot.command(name='eval')
async def _eval(ctx, *, body):
    """Evaluates python code"""
    if not dev_check(ctx.author.id):
        return await ctx.send("You cannot use this because you are not a developer.")
    env = {
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': bot._last_result,
        'source': inspect.getsource
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()
    err = out = None

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    def paginate(text: str):
        '''Simple generator that paginates text.'''
        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != '', pages))

    try:
        exec(to_compile, env)
    except Exception as e:
        err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        return await ctx.message.add_reaction('\u2049')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        if TOKEN in value:
            value = value.replace(TOKEN,"[lol]")
        if ret is None:
            if value:
                try:

                    out = await ctx.send(f'```py\n{value}\n```')
                except:
                    paginated_text = paginate(value)
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')
        else:
            bot._last_result = ret
            try:
                out = await ctx.send(f'```py\n{value}{ret}\n```')
            except:
                paginated_text = paginate(f"{value}{ret}")
                for page in paginated_text:
                    if page == paginated_text[-1]:
                        out = await ctx.send(f'```py\n{page}\n```')
                        break
                    await ctx.send(f'```py\n{page}\n```')

    if out:
        await ctx.message.add_reaction('\u2705')  # tick
    elif err:
        await ctx.message.add_reaction('\u2049')  # x
    else:
        await ctx.message.add_reaction('\u2705')

  

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="dat orange bot invite link!", color=0xce1414)
    embed.description = "https://discordapp.com/api/oauth2/authorize?client_id=439919013766758420&permissions=305454295&scope=bot :smile: :muscle::skin-tone-2:"
    await ctx.send(embed = embed)

@bot.command()
async def support(ctx):
    embed = discord.Embed(title='Bravo Zulu Support Server', color=0xce1414)
    embed.description = "https://discord.gg/EvjMmPB \n https://github.com/granthood/bravo_zulu_bot"
    await ctx.send(embed=embed)


@bot.command()
async def contributors(ctx):
    embed = discord.Embed(title="Bravo Zulu Developers", color=0xce1414)
    embed.description = "Main Devs: \n Bravo Zulu#0638 \n FreeTNT#5796 \n CyRIC#0847 \n Sub Devs: \n L3NNY#4519 \n dat banana boi#1982 \n Ice#1234"
    await ctx.send(embed=embed)
        
        
@bot.command()
async def coin(ctx):
    choice = random.randint(1, 2)
    if choice == 1:
        embed = discord.Embed(title="**Heads**")
        await ctx.send(embed=embed)
    if choice == 2:
        embed = discord.Embed(title="**Tails**")
        return await ctx.send(embed=embed)
    
@bot.command(pass_context=True)
async def coclineup(ctx):
    embed = discord.Embed(title=random.choice([
        "5v5", "10v10", "15v15", "20v20",
        "30v30", "40v40", "50v50"]), color=0xce1414)
    await ctx.send(embed=embed)
    
@bot.command()
async def hack(ctx, user: discord.Member):
        """Hack someone's account! Try it!"""
        msg = await ctx.send(f"Hacking! Target: {user}")
        await asyncio.sleep(2)
        await msg.edit(content=f"Accessing {user}'s Files... [▓▓    ]")
        await asyncio.sleep(2)
        await msg.edit(content=f"Accessing {user}'s Files... [▓▓▓   ]")
        await asyncio.sleep(2)
        await msg.edit(content=f"Accessing{user}'s Files... [▓▓▓▓▓ ]")
        await asyncio.sleep(2)
        await msg.edit(content=f"Accessing {user}'s Files COMPLETE! [▓▓▓▓▓▓]")
        await asyncio.sleep(2)
        await msg.edit(content=f"Retrieving {user}'s Login Info... [▓▓▓    ]")
        await asyncio.sleep(3)
        await msg.edit(content=f"Retrieving {user}'s Login Info... [▓▓▓▓▓ ]")
        await asyncio.sleep(3)
        await msg.edit(content=f"Retrieving  {user}'s Login Info... [▓▓▓▓▓▓ ]")
        await asyncio.sleep(4)
        await msg.edit(content=f"An error has occurred hacking {user}'s account. Please try again later. ❌") 
        
        
        

    
    


bot.run(os.environ.get('TOKEN'))
