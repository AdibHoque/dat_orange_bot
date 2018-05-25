import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import youtube_dl


youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music:
  def __init__(self, bot):
      self.bot = bot
        
  if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus.so')
        
  @commands.command()
  async def connect(self, ctx):
      '''Connects the bot to your current voice channel.'''
      if ctx.author.voice is None:
          return await ctx.send("Looks like you aren't connected to a voice channel yet! Where do I join?")
      if ctx.voice_client is None:
          await ctx.author.voice.channel.connect()
          await ctx.send(f"Successfully connected to Voice Channel **{ctx.author.voice.channel.name}**. :white_check_mark:")
      else:
          await ctx.voice_client.move_to(ctx.author.voice.channel)
          await ctx.send(f"Successfully connected to Voice Channel: **{ctx.author.voice.channel.name}**. :white_check_mark:")
    
  @commands.command()
  async def stop(self, ctx):
      """Stops and disconnects the bot from voice"""
      await ctx.voice_client.disconnect()
    
def setup(bot):
  bot.add_cog(Music(bot))
