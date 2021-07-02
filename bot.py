import discord
import yaml
from discord.ext import tasks, commands

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

from util.inspect import process_msg

with open("conf.yaml", "r") as c: cfg = yaml.safe_load(c) 
bot = commands.Bot(command_prefix="::")
slash = SlashCommand(bot, sync_commands=True)
sites = cfg["sites"]

# Slash Command
@slash.slash(name="inlay",
             description="Embed or get a direct link for a video",
             options=[create_option( name="url", description="URL to page with a video\
                                     to embed", option_type=3, required=True )])
async def inlay(ctx, url: str):
    await ctx.send(content=f"Processing: {url}")
    embed = process_msg(url, sites, direct=True)
    
    if embed:
        await ctx.channel.send(content=embed)
    else:
        await ctx.channel.send(content="Could not find or embed video 😥")

# Automatic (On Matching URL)
if cfg["automatic"]:
    @bot.event
    async def on_message(ctx):
        if not ctx.author == bot.user:
            embed = process_msg(ctx.content, sites, True)

            if embed:
                await ctx.channel.send(content=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name=cfg["status"]))

if __name__ == "__main__":
    bot.run(cfg["secrets"]["discord"]["token"])