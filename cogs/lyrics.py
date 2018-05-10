from bot_log import log
import discord
from discord.ext import commands
import asyncio
import requests
from bs4 import BeautifulSoup
import os


class Lyrics:
    def __init__(self,bot):
        self.bot = bot
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
        self.link = "https://search.azlyrics.com/search.php?q="
    
    async def getlyrics(self,song,channel,user):
        await self.bot.wait_until_ready()
        get_request_search = requests.get(self.link + song+ "&w=songs&p=1" , headers=self.headers)
        soup_search = BeautifulSoup(get_request_search.content,'html.parser')
        try:
            link_from_search  = soup_search.find('td',{'class':'text-left visitedlyr'}).find('a')
            get_request_lyrics = requests.get(link_from_search['href'],headers=self.headers)
            soup_lyrics = BeautifulSoup(get_request_lyrics.content,'html.parser')
            
            lyrics_text = soup_lyrics.find('div',{'class':'col-xs-12 col-lg-8 text-center'}).find('div',None).text
            header_text = soup_lyrics.find('div',{'class':'lyricsh'}).text       
            log.debug('header : ' + header_text)
            log.debug('lryics : ' + lyrics_text)
        
            await self.bot.send_message(channel,user.mention+" friend i got the lyrics..here is it and also i send a copy as a file in pm")
            f = open(song.replace("+"," ")+'.txt','w')
            f.write('\t\t'+header_text+'\n\n'+lyrics_text)
            f.close()
            await self.bot.send_file(user,song+'.txt')
            os.remove(song+'.txt')
            embed = discord.Embed(title=header_text,description=lyrics_text,color=0xa500ff)             
            await self.bot.send_message(channel,embed=embed)
        
        except Exception as e:
            log.exception(str(e))
            await self.bot.send_message(channel,"Sorry :( i can't find it")
    
    @commands.command(pass_context=True)
    async def lyrics(self,ctx,*,song:str):
        await self.bot.say("Lemme look wait....")
        song = song.replace(" ","+")
        await self.bot.loop.create_task(self.getlyrics(song,ctx.message.channel,ctx.message.author))
        
        
def setup(bot): 
    bot.add_cog(Lyrics(bot))
