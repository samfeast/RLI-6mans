import discord
from discord.ext import commands
import asyncio
from os import listdir
import token_file

PREFIX = ">"
# Imports bot token from config.py (so it's hidden on GitHub)
TOKEN = token_file.TOKEN
# Guild ID of server for slash commands to be registered in
GUILD_ID = 846538497087111169

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
# Initilises slash command tree
tree = bot.tree


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} [{bot.user.id}]")
    print("Servers:")
    for guild in bot.guilds:
        print(f"\t{guild.name}")


# Sync all slash commands to be used in the provided server
# Only use when a new command is added, or the name/description of an existing command is changed
@bot.command()
async def synclocal(ctx):
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    await ctx.send("Slash commands synced.")


# Reloads a cog (cog argument does not need to contain _cog.py)
@bot.command()
async def reload(ctx, cog):
    try:
        await bot.reload_extension(f"{cog.lower()}_cog")
        await ctx.send(f"{cog.capitalize()}_cog reloaded successfully.")
    except Exception as e:
        print(f"Failed to reload {cog}_cog. This isn't supposed to happen...")
        print(f"{type(e).__name__}: {e}")


# Reloads all cogs
@bot.command()
async def reload_all(ctx):
    cogs = [f[:-3] for f in listdir() if "cog" == f[-6:-3]]
    for cog in cogs:
        try:
            await bot.reload_extension(cog)
            await ctx.send(f"{cog.capitalize()} reloaded successfully.")
        except Exception as e:
            print(f"Failed to reload {cog}. This isn't supposed to happen...")
            print(f"{type(e).__name__}: {e}")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong! (from a prefix command)")


@tree.command(description="Ping the bot.", guild=discord.Object(id=GUILD_ID))
async def ping_main(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)


# New asynchronous way of running the bot and loading cogs in d.py 2.0
async def main():
    async with bot:
        cogs = [f[:-3] for f in listdir() if "cog" == f[-6:-3]]
        print("Cogs:")
        for cog in cogs:
            try:
                await bot.load_extension(cog)
                print(f"\t{cog}")
            except Exception as e:
                print(f"Failed to load {cog}")
                print(f"{type(e).__name__}: {e}")
        await bot.start(TOKEN)


asyncio.run(main())
