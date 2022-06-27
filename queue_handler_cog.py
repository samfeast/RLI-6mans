import discord
from discord.ext import commands
from discord import app_commands
import json

with open("json/config.json", "r") as read_file:
    config = json.load(read_file)

elite_channel_id = config["tiers"]["elite"]
premier_channel_id = config["tiers"]["premier"]
championship_channel_id = config["tiers"]["championship"]

elite_queue = []
premier_queue = []
championship_queue = []

all_tier_queue = []


class queue_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Ping the elite cog.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def ping_elite(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    @app_commands.command(description="Join the queue.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def q(self, interaction: discord.Interaction):

        if interaction.user.id in all_tier_queue:
            await interaction.response.send_message(
                "Sorry! You can't be in two queues at the same time."
            )
        else:
            if interaction.channel_id == elite_channel_id:
                await self.add_to_queue(interaction, interaction.user.id, elite_queue)
            elif interaction.channel_id == premier_channel_id:
                print("Join premier queue")
            elif interaction.channel_id == championship_channel_id:
                print("Join championship queue")
            else:
                print("This is not a registered channel")

    async def add_to_queue(self, interaction, user, queue):
        if user in queue:
            await interaction.response.send_message("You're already in the queue")
        else:
            queue.append(user)
            if len(queue) == 6:
                await interaction.response.send_message("Queue popped")
            else:
                await interaction.response.send_message("Move")


async def setup(bot):
    await bot.add_cog(queue_handler(bot))
