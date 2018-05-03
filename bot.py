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
        return "bz."
    pre = l.get('prefix', "bz.")
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
        await bot.change_presence(activity=discord.Game(name='bz.help with my friends!'))
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


@bot.command(pass_context=True, aliases=["clear"])
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
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member):
    try:
        await ctx.send(f'**{user.name}** is now banned from the server!')
        await ctx.guild.ban(user)
    except discord.Forbidden:
        await ctx.send(f"Bravo Zulu lacks the permission to ban **{user.name}**.")
    except commands.errors.MissingPermissions:
        await ctx.send("no perms bro")
        

@bot.command
async def warn(ctx, user: discord.Member, reason):
    await ctx.send("You have been warned by {} for {}".format(ctx.author.name, reason))
    
@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, user: discord.Member = None):
    if user is None:
        return await ctx.send("Please tag the user in order to mute them.")
    try:
        await ctx.channel.set_permissions(user, send_messages=False)
        return await ctx.send(f"{user.mention} has been muted. Unmute them when you see fit.")
    except commands.errors.MissingPermissions:
        return await ctx.send("You lack perms")
    except discord.Forbidden:
        return await ctx.send("I lack the **Manage channel** permission.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, user: discord.Member = None):
    if user is None:
        return await ctx.send("Please tag the user in order to unmute them")
    try:
        await ctx.channel.set_permissions(user, send_messages=True)
        return await ctx.send(f"{user.mention} has been unmuted. Enjoy freedom. While it lasts.")
    except commands.errors.MissingPermissions:
        return await ctx.send("You lack perms")
    except discord.Forbidden:
        return await ctx.send("I lack the **Manage Channel** permission.")    

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="Bravo Zulu invite link!", color=0xce1414)
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
        
        
@bot.command()
async def coin(ctx):
    choice = random.randint(1, 2)
    if choice == 1:
        embed = discord.Embed(title="**Heads**")
        await ctx.send(embed=embed)
    if choice == 2:
        embed = discord.Embed(title="**Tails**")
        return await ctx.send(embed=embed)
    
    
@bot.command()
async def prifles(ctx):
    """Veiw the stats of AR's in PUBG Mobile"""
    embed = discord.Embed(title="AR Stats", description="AR Stats for AR's in PUBG Mobile", color=0xce1414)
    embed.add_field(name="Weapon", value="Groza\nAKM\ndp28\nauga3\nM16A4\nM416\nScar-L\nM249")
    embed.add_field(name="Use bz.<weapon name> for more info")
    await ctx.send(embed=embed)

@bot.command()
async def groza(ctx):
    """Veiw the stats of the Groza AR"""
    embed = discord.Embed(title="Groza Stats", description="Stats for the Groza AR", color=0xce1414)
    embed.add_field(name="Base Damage", value="49")
    embed.add_field(name="Fire Rate", value="0.08 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="843")
    embed.add_field(name="TTK (Time to Kill)", value="0.24 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="7.62")
    await ctx.send(embed=embed)

@bot.command()
async def akm(ctx):
    """Veiw the stats of the AKM AR"""
    embed = discord.Embed(title="AKM Stats", description="Stats for the AKM AR", color=0xce1414)
    embed.add_field(name="Base Damage", value="49")
    embed.add_field(name="Fire Rate", value="0.1 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="490")
    embed.add_field(name="TTK (Time to Kill)", value="0.3 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="7.62")
    await ctx.send(embed=embed)

@bot.command()
async def dp28(ctx):
    """Veiw the stats of the DP-28 AR"""
    embed = discord.Embed(title="DP-28 Stats", description="Stats for the DP-28 AR", color=0xce1414)
    embed.add_field(name="Base Damage", value="49")
    embed.add_field(name="Fire Rate", value="0.08 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="450")
    embed.add_field(name="TTK (Time to Kill)", value="0.33 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="7.62")
    await ctx.send(embed=embed)

@bot.command()
async def auga3(ctx):
    """Veiw the stats of the Aug A3 AR"""
    embed = discord.Embed(title="Aug A3 Stats", description="Stats for the Aug A3 AR", color=0xce1414)
    embed.add_field(name="Base Damage", value="44")
    embed.add_field(name="Fire Rate", value="0.095 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="513")
    embed.add_field(name="TTK (Time to Kill)", value="0.26 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="5.56")
    await ctx.send(embed=embed)

@bot.command()
async def m16a4(ctx):
    """Veiw the stats of the M16A4 AR"""
    embed = discord.Embed(title="M16A4 Stats", description="Stats for the M16A4 AR", color=0xce1414)
    embed.add_field(name="Base Damage", value="44")
    embed.add_field(name="Fire Rate", value="0.075 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="587")
    embed.add_field(name="TTK (Time to Kill)", value="0.23 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="5.56")
    await ctx.send(embed=embed)

@bot.command()
async def m416(ctx):
    """Veiw the stats of the M416 AR"""
    embed = discord.Embed(title="M416 Stats", description="Stats for the M416 AR", color=0xce1414)
    embed.add_field(name="Base Damage", value="49")
    embed.add_field(name="Fire Rate", value="0.085 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="513")
    embed.add_field(name="TTK (Time to Kill)", value="0.26 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="5.56")
    await ctx.send(embed=embed)

@bot.command()
async def scarl(ctx):
    """Veiw the stats of the Scar-L AR"""
    embed = discord.Embed(title="Scar-L Stats", description="Stats for the Scar-L AR", color=0xce1414)
    embed.add_field(name="Base Damage", value="49")
    embed.add_field(name="Fire Rate", value="0.095 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="458")
    embed.add_field(name="TTK (Time to Kill)", value="0.29 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="5.56")
    await ctx.send(embed=embed)

@bot.command()
async def m249(ctx):
    """Veiw the stats of the M249 LMG"""
    embed = discord.Embed(title="Groza Stats", description="Stats for the M249 LMG", color=0xce1414)
    embed.add_field(name="Base Damage", value="49")
    embed.add_field(name="Fire Rate", value="0.075 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="600")
    embed.add_field(name="TTK (Time to Kill)", value="0.23 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="5.56")
    await ctx.send(embed=embed)@bot.command(pass_context=True)
async def fortune(ctx):
    embed = discord.Embed(title=random.choice([
        "It is certain", "As I see it, yes ", "It is decidedly so ",
        "Without a doubt ", "Yes definitely ", "You may rely on it ",
        "Most likely ", "Outlook good ", "Yes ", ":thumbsup: ",
        "Reply hazy try again ", "Ask again later", "Better not tell you now ",
        "Cannot predict now ", "Concentrate and ask again", "Don't count on it",
        "My reply is no ", "My sources say no ", "Outlook not so good ", "Very doubtful ",
        "NO. JUST NO."]), color=0xce1414)
    await ctx.send(embed=embed)
    
@bot.command()
async def psmg(ctx):
    """Veiw the stats of SMG's in PUBG Mobile"""
    embed = discord.Embed(title="SMG Stats", description="SMG Stats for SMG's in PUBG Mobile", color=0xce1414)
    embed.add_field(name="Weapons", value="Tommy Gun\nUMP9\nVector\nUZI")
    embed.add_field(name="Usage", value="prefix + <name of weapon> NOTE: use all lowercase and no hyphons (-)")
    await ctx.send(embed=embed)

@bot.command()
async def tommygun(ctx):
    """Veiw the stats of the Tommy Gun SMG"""
    embed = discord.Embed(title="Tommy Gun Stats", description="Stats for the Tommy Gun SMG", color = 0xce1414)
    embed.add_field(name="Base Damage", value="40")
    embed.add_field(name="Fire Rate", value="0.085 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="487")
    embed.add_field(name="TTK (Time to Kill)", value="0.34 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="5")
    embed.add_field(name="STK (Head)", value="3")
    embed.add_field(name="Ammo Type", value=".45 ACP")
    await ctx.send(embed=embed)

@bot.command()
async def ump9(ctx):
    """Veiw the stats of the UMP9 SMG"""
    embed = discord.embed(title="UMP9 Stats", description="Stats for the UMP9 SMG", color=0xce1414)
    embed.add_field(name="Base Damage", value="35")
    embed.add_field(name="Fire Rate", value="0.092 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="412")
    embed.add_field(name="TTK (Time to Kill)", value="0.37 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="5")
    embed.add_field(name="STK (Head)", value="3")
    embed.add_field(name="Ammo Type", value="9 MIL")
    await ctx.send(embed=embed)


@bot.command()
async def vector(ctx):
    """Veiw the stats of the Vector SMG"""
    embed = discord.Embed(title="Vector Stats", description="Stats for the Vector SMG", color=0xce1414)
    embed.add_field(name="Base Damage", value="33")
    embed.add_field(name="Fire Rate", value="0.065 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="606")
    embed.add_field(name="TTK (Time to Kill)", value="0.27 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="6")
    embed.add_field(name="STK (Head)", value="3")
    embed.add_field(name="Ammo Type", value=".45 ACP")
    await ctx.send(embed=embed)

@bot.command()
async def uzi(ctx):
    """Veiw the stats of the UZI SMG"""
    embed = discord.Embed(title="UZI SMG", description="Stats for the UZI SMG", color=0xce414)
    embed.add_field(name="Base Damage", value="25")
    embed.add_field(name="Fire Rate", value="0.048 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="521")
    embed.add_field(name="TTK (Time to Kill)", value="0.29 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="7")
    embed.add_field(name="STK (Head)", value="4")
    embed.add_field(name="Ammo Type", value="(9 MIL")
    await ctx.send(embed=embed)

@bot.command()
async def psniper(ctx):
    """View the stats of SR's in PUBG Mobile"""
    embed = discord.Embed(title="SR Stats", description="SR Stats for SR's in PUBG Mobile", color=0xce1414)
    embed.add_field(name="Weapons", value="AWM\nM24\nKar98k\Win54\nMK14\nSKS\nMini 14\nVSS")
    embed.add_field(name="Usage", value="prefix + <name of weapon> NOTE: use all lowercase and no hyphons (-)")
    await ctx.send(embed=embed)

@bot.command()
async def awm(ctx):
    """Veiw the stats of the AWM SR"""
    embed = discord.Embed(title="AWM SR", description="Stats for the AWM SR", color=0xce414)
    embed.add_field(name="Base Damage", value="120")
    embed.add_field(name="Fire Rate", value="1.85 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="68")
    embed.add_field(name="TTK (Time to Kill)", value="1.85 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="2")
    embed.add_field(name="STK (Head)", value="1")
    embed.add_field(name="Ammo Type", value=".Magnum")
    await ctx.send(embed=embed)

@bot.command()
async def m24(ctx):
    """Veiw the stats of the M24 SR"""
    embed = discord.Embed(title="M24 SR", description="Stats for the M24 SR", color=0xce414)
    embed.add_field(name="Base Damage", value="88")
    embed.add_field(name="Fire Rate", value="1.8 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="48")
    embed.add_field(name="TTK (Time to Kill)", value="1.8 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="2")
    embed.add_field(name="STK (Head)", value="1")
    embed.add_field(name="Ammo Type", value="7.62")
    await ctx.send(embed=embed)

@bot.command()
async def kar98k(ctx):
    """Veiw stats of the Kar98k SR"""
    embed = discord.Embed(title="Kar98k SR", description="Stats for the Kar98k SR", color=0xce414)
    embed.add_field(name="Base Damage", value="75")
    embed.add_field(name="Fire Rate", value="1.9 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="39")
    embed.add_field(name="TTK (Time to Kill)", value="3.8 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="2")
    embed.add_field(name="STK (Head)", value="1")
    embed.add_field(name="Ammo Type", value="7.62")
    await ctx.send(embed=embed)

@bot.command()
async def win54(ctx):
    """Veiw stats of the Win54 SR"""
    embed = discord.Embed(title="Win54 SR", description="Stats for the Win54 SR", color=0xce414)
    embed.add_field(name="Base Damage", value="66")
    embed.add_field(name="Fire Rate", value="0.8 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="110")
    embed.add_field(name="TTK (Time to Kill)", value="1.2 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="3")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="Unknown")
    await ctx.send(embed=embed)

@bot.command()
async def mk14(ctx):
    """Veiw stats of the MK14 SR"""
    embed = discord.Embed(title="MK14 SR", description="Stats for the MK14 SR", color=0xce1414)
    embed.add_field(name="Base Damage", value="68")
    embed.add_field(name="Fire Rate", value="0.09 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="678")
    embed.add_field(name="TTK (Time to Kill)", value="0.18 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="2")
    embed.add_field(name="STK (Head)", value="3")
    embed.add_field(name="Ammo Type", value="7.62")
    await ctx.send(embed=embed)

@bot.command()
async def sks(ctx):
    """Veiw stats for the SKS SR"""
    embed = discord.Embed(title="SKS SR", description="Stats for the SKS SR", color=0xce414)
    embed.add_field(name="Base Damage", value="57")
    embed.add_field(name="Fire Rate", value="0.133 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="428")
    embed.add_field(name="TTK (Time to Kill)", value="0.27 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="3")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="7.62")
    await ctx.send(embed=embed)

@bot.command()
async def mini14(ctx):
    """Veiw stats for the Mini 14 SR"""
    embed = discord.Embed(title="Mini 14 SR", description="Stats for the Mini 14 SR", color=0xce414)
    embed.add_field(name="Base Damage", value="48")
    embed.add_field(name="Fire Rate", value="0.133 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="338")
    embed.add_field(name="TTK (Time to Kill)", value="0.4 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="5.56")
    await ctx.send(embed=embed)

@bot.command()
async def vss(ctx):
    """Veiw stats for the VSS SR"""
    embed = discord.Embed(title="VSS SR", description="Stats for the VSS SR", color=0xce414)
    embed.add_field(name="Base Damage", value="40")
    embed.add_field(name="Fire Rate", value="0.086 sec")
    embed.add_field(name="DPS (Damage Per Second)", value="467")
    embed.add_field(name="TTK (Time to Kill)", value="0.34 sec")
    embed.add_field(name="STK (Chest) (Shots to Kill)", value="6")
    embed.add_field(name="STK (Head)", value="2")
    embed.add_field(name="Ammo Type", value="9 MIL")
    await ctx.send(embed=embed)
    
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
