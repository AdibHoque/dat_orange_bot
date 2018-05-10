import discord
import sys
import os
import io
import json
import ezjson
import random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Economy:
    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.session
        self.db = self.bot.db
        with open('data/apikeys.json') as f:
            x = json.loads(f.read())
        self.dbl = x['dblapi']

    async def add_points(self, user, points):
        x = await self.db.datbananabot.economy.find_one({"user": user.id})
        total = int(x['points']) + points
        await self.db.datbananabot.economy.update_one({"user": user.id}, {"$set": {"points": total}}, upsert=True)
        

    async def is_registered(self, user):
        x = await self.db.datbananabot.economy.find_one({"user": user.id})
        if x is None:
            return False
        else:
            return True
            
            
            
            
def setup(bot):
  bot.add_cog(Economy(bot))
