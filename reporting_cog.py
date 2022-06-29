from asyncore import write
import discord
from discord.ext import commands
from discord import app_commands
import json


class reporting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping cog command
    @app_commands.command(description="Ping the elite cog.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def ping_reporting(self, interaction: discord.Interaction, the_thing: str):
        # await interaction.response.send_message("Pong!", ephemeral=True)
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label=the_thing,
                style=discord.ButtonStyle.green,
            )
        )


async def setup(bot):
    await bot.add_cog(reporting(bot))
