from moto.motor_asyncio import AsyncioMotorClient
import os

db = AsyncioMotorClient(os.environ.get("ECODB"))
bot.db = db.datorangebot
