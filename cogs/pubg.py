import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

class PUBG:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def pubg(self, ctx):
        """Usage: [prefix] + [gun]"""
        await ctx.send("Usage: [prefix] + [gun} Note: Use all lowercase and no hyphons (-)")

    @pubg.command()
    async def ars(self, ctx):
        """Veiw the stats of AR's in PUBG Mobile"""
        embed = discord.Embed(title="AR Stats", description="AR Stats for AR's in PUBG Mobile", color=0xce1414)
        embed.add_field(name="Weapons", value="Groza\nAKM\nDP-28\nAUG A3\nM16A4\nM416\nScar-L\nM249")
        embed.add_field(name="Usage", value="prefix + <pubg> <name of weapon> NOTE: use all lowercase and no hyphons (-).")
        await ctx.send(embed=embed)

    @pubg.command()
    async def groza(self, ctx):
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

    @pubg.command()
    async def akm(self, ctx):
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

    @pubg.command()
    async def dp28(self, ctx):
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

    @pubg.command()
    async def auga3(self, ctx):
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

    @pubg.command()
    async def m16a4(self, ctx):
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

    @pubg.command()
    async def m416(self, ctx):
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

    @pubg.command()
    async def scarl(self, ctx):
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

    @pubg.command()
    async def m249(self, ctx):
        """Veiw the stats of the M249 LMG"""
        embed = discord.Embed(title="Groza Stats", description="Stats for the M249 LMG", color=0xce1414)
        embed.add_field(name="Base Damage", value="49")
        embed.add_field(name="Fire Rate", value="0.075 sec")
        embed.add_field(name="DPS (Damage Per Second)", value="600")
        embed.add_field(name="TTK (Time to Kill)", value="0.23 sec")
        embed.add_field(name="STK (Chest) (Shots to Kill)", value="4")
        embed.add_field(name="STK (Head)", value="2")
        embed.add_field(name="Ammo Type", value="5.56")
        await ctx.send(embed=embed)

    @pubg.command()
    async def smg(self, ctx):
        """Veiw the stats of SMG's in PUBG Mobile"""
        embed = discord.Embed(title="SMG Stats", description="SMG Stats for SMG's in PUBG Mobile", color=0xce1414)
        embed.add_field(name="Weapons", value="Tommy Gun\nUMP9\nVector\nUZI")
        embed.add_field(name="Usage", value="prefix + <pubg> <name of weapon> NOTE: use all lowercase and no hyphons (-)")
        await ctx.send(embed=embed)

    @pubg.command()
    async def tommygun(self, ctx):
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

    @pubg.command()
    async def ump9(self, ctx):
        """Veiw the stats of the UMP9 SMG"""
        embed = discord.Embed(title="UMP9 Stats", description="Stats for the UMP9 SMG", color=0xce1414)
        embed.add_field(name="Base Damage", value="35")
        embed.add_field(name="Fire Rate", value="0.092 sec")
        embed.add_field(name="DPS (Damage Per Second)", value="412")
        embed.add_field(name="TTK (Time to Kill)", value="0.37 sec")
        embed.add_field(name="STK (Chest) (Shots to Kill)", value="5")
        embed.add_field(name="STK (Head)", value="3")
        embed.add_field(name="Ammo Type", value="9 MIL")
        await ctx.send(embed=embed)

    
    @pubg.command()
    async def vector(self, ctx):
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

    @pubg.command()
    async def uzi(self, ctx):
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

    @pubg.command()
    async def sniper(self, ctx):
        """View the stats of SR's in PUBG Mobile"""
        embed = discord.Embed(title="SR Stats", description="SR Stats for SR's in PUBG Mobile", color=0xce1414)
        embed.add_field(name="Weapons", value="AWM\nM24\nKar98k\nWin54\nMK14\nSKS\nMini 14\nVSS")
        embed.add_field(name="Usage", value="prefix + <pubg> <name of weapon> NOTE: use all lowercase and no hyphons (-)")
        await ctx.send(embed=embed)

    @pubg.command()
    async def awm(self, ctx):
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

    @pubg.command()
    async def m24(self, ctx):
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

    @pubg.command()
    async def kar98k(self, ctx):
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

    @pubg.command()
    async def win54(self, ctx):
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

    @pubg.command()
    async def mk14(self, ctx):
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

    @pubg.command()
    async def sks(self, ctx):
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

    @pubg.command()
    async def mini14(self, ctx):
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

    @pubg.command()
    async def vss(self, ctx):
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


def setup(bot):
    bot.add_cog(PUBG(bot))
