import logging

import discord
import yaml
from discord.ext import commands

from inlay.embed import Site, generate_embed, parse_site

with open("conf.yaml", "r") as c:
    cfg = yaml.safe_load(c)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="::", intents=intents)
configured_sites = [Site(**site) for site in cfg["sites"]]

logger = logging.getLogger("inlay")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("inlay.log")
fh.setLevel(logging.DEBUG)

logger.addHandler(fh)


@bot.tree.command(name="url", description="Embed or get a direct link for a video")
async def inlay(ctx, url: str):
    embed = None
    logger.info(f"Received URL: {url}")
    async with ctx.channel.typing():
        parsed_site = parse_site(url, configured_sites)
        if parsed_site.url:
            logger.info(f"Retrieved: {url}")
            embed = generate_embed(parsed_site, direct=True)
    if embed:
        await ctx.channel.send(content=embed)
    else:
        await ctx.channel.send(content="Could not find or embed video 😥")


# Automatic (On Matching URL)
if cfg["automatic"]:

    @bot.event
    async def on_message(ctx):
        if not ctx.author == bot.user:
            embed_url = None
            parsed_site = parse_site(ctx.content, configured_sites)
            if parsed_site and parsed_site.name:  # embeddable
                logging.debug(
                    f"User {ctx.author} sent matching site {parsed_site.name} for URL {parsed_site.url} from guild {ctx.guild.name} - {ctx.guild.id}"
                )
                # async with ctx.channel.typing():
                embed_url = generate_embed(parsed_site)
            if embed_url:
                logger.debug(f"Generated embed: {embed_url} for site")
                if parsed_site.spoiler:
                    embed_url = f"||{embed_url} ||"
                if cfg["reply"]:
                    await ctx.reply(embed_url, mention_author=cfg["mention"])
                else:
                    await ctx.channel.send(content=embed_url)
                if cfg["delete"]:
                    await ctx.delete()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name=cfg["status"]))
    await bot.tree.sync()


if __name__ == "__main__":
    bot.run(cfg["secrets"]["discord"]["token"])
