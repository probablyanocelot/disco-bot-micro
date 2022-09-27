import discord
import asyncio
import sys
import pafy
import requests
import os
import youtube_dl
from random import choice
from dotenv import load_dotenv

from config import FFMPEG_OPTIONS, TOKEN
from search_yt import yt_query, YT_API_KEY, get_vid_name
# from discord import app_commands
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


# This example requires the 'message_content' privileged intent for prefixed commands.


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    # Bind to ipv4 since ipv6 addresses cause issues at certain times
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.AudioSource, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            # Takes the first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


song_dict = dict()
counter = {'count': 0}


class Music(commands.Cog):
    def __init__(self, bot_: commands.Bot):
        self.bot = bot_

    async def get_guild_dict(self, ctx):
        # guild == server; this is to enable multiple servers to use the bot
        guild = ctx.guild
        if not guild.name in song_dict.keys():
            song_dict[guild.name] = {}

        guild_dict = song_dict[guild.name]
        return guild_dict

    @commands.command()
    async def join(self, ctx: commands.Context, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str, by_user=True):
        """Streams from YouTube"""

        guild_dict = await self.get_guild_dict(ctx)

        if by_user:
            print(query)

            # try:
            url = await yt_query(YT_API_KEY, query)
            # except:
            # await ctx.send("No results found for {}".format(query))
            # return

        if not by_user:
            # url = guild_dict[counter['count']]['url']
            pass

        try:
            song = pafy.new(url).getbestaudio()
        except:
            await ctx.send(f'Cannot get streaming data for {query}')
            # return

        guild_dict[len(guild_dict)] = {'title': song.title, 'url': url}

        try:
            if ctx.voice_client.is_playing():
                await ctx.send('**Queued:** {}'.format(song.title))
                return
        except AttributeError:
            return

        try:
            guild_dict[len(guild_dict)] = {
                'title': song.title, 'url': url
            }
        except AttributeError:
            await ctx.send('No song found.')
            return

        song = guild_dict[counter['count']]

        print(f'song_dict: {song_dict}')
        print(f'guild_dict: {guild_dict}')

        # await player(ctx, song['url'], song['title'])

        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song['url'], **FFMPEG_OPTIONS))

        msg = await ctx.send('**Now playing:** {}'.format(song['title']))

        ctx.voice_client.play(source, after=lambda e: print(
            f"Player error: {e}") if e else None)

        await ctx.send(f"Now playing: {song['title']}")

    @commands.command()
    async def yt(self, ctx: commands.Context, *, url: str):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(
                f"Player error: {e}") if e else None)

        await ctx.send(f"Now playing: {player.title}")

    @commands.command()
    async def stream(self, ctx: commands.Context, *, url: str):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                f"Player error: {e}") if e else None)

        await ctx.send(f"Now playing: {player.title}")

    @commands.command()
    async def volume(self, ctx: commands.Context, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect(force=True)

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("%"),
    description="Relatively simple music bot example",
    intents=intents,
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


bot.add_cog(Music(bot))
bot.run(DISCORD_TOKEN)
