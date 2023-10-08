import discord
import yaml
from discord.ext import commands
from discord import app_commands

import logging

from util.inspect import process_url, process_site

with open("conf.yaml", "r") as c: cfg = yaml.safe_load(c) 
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="::", intents=intents)
sites = cfg["sites"]

logger = logging.getLogger('inlay')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)

logger.addHandler(fh)

@bot.tree.command(
    name="url",
    description="Embed or get a direct link for a video"
)
async def inlay(ctx, url: str):
    embed = None
    logger.info(f"Received URL: {url}")
    async with ctx.channel.typing():
        site, url = process_site(url, sites)
        if url:
            logger.info(f"Retrieved: {url}")
            embed = process_url(url, site, direct=True)
    if embed:
        await ctx.channel.send(content=embed)
    else:
        await ctx.channel.send(content="Could not find or embed video 😥")

# Automatic (On Matching URL)
if cfg["automatic"]:
    @bot.event
    async def on_message(ctx):
        if not ctx.author == bot.user:
            embed = None
            site, url, spoiler = process_site(ctx.content, sites)
            if site and url:
                logger.debug(f"User {ctx.author} sent matching site {site} for URL {url} from guild {ctx.guild.name} - {ctx.guild.id}")
                async with ctx.channel.typing():
                    embed = process_url(url, site)
            if embed: 
                # embed = f"Sent by *{ctx.author.nick}*\n" + embed
                logger.debug(f"Generated embed: {embed} for site")
                if spoiler:
                    embed = f"||{embed} ||"
                if cfg["reply"]: 
                    await ctx.reply(embed, mention_author=cfg["mention"])
                else: 
                    await ctx.channel.send(content=embed)

                if cfg["delete"]:
                    await ctx.delete()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name=cfg["status"]))
    await bot.tree.sync() 

if __name__ == "__main__":
    bot.run(cfg["secrets"]["discord"]["token"])