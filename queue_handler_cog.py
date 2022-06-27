import discord
from discord.ext import commands
from discord import app_commands
import json

with open("json/config.json", "r") as read_file:
    config = json.load(read_file)

elite_channel_id = config["tiers"]["elite"]
premier_channel_id = config["tiers"]["premier"]
championship_channel_id = config["tiers"]["championship"]
casual_channel_id = config["tiers"]["casual"]
elite_logs_channel_id = config["tiers"]["elite_logs"]
premier_logs_channel_id = config["tiers"]["premier_logs"]
championship_logs_channel_id = config["tiers"]["championship_logs"]
casual_logs_channel_id = config["tiers"]["casual_logs"]

elite_queue = []
premier_queue = []
championship_queue = []
casual_queue = []

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
                "Sorry! You are already in a 6mans queue."
            )
        else:
            if interaction.channel_id == elite_channel_id:
                await self.add_to_queue(interaction, interaction.user, elite_queue)
            elif interaction.channel_id == premier_channel_id:
                await self.add_to_queue(interaction, interaction.user, premier_queue)
            elif interaction.channel_id == championship_channel_id:
                await self.add_to_queue(
                    interaction, interaction.user, championship_queue
                )
            elif interaction.channel_id == casual_channel_id:
                await self.add_to_queue(interaction, interaction.user, casual_queue)
            else:
                await interaction.response.send_message(
                    "Queuing is not enabled in this channel."
                )

    @app_commands.command(description="Add a player to the queue.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def add(self, interaction: discord.Interaction, user: discord.User):

        if user.id in all_tier_queue:
            await interaction.response.send_message(
                "Sorry! The user is already in a 6mans queue."
            )
        else:
            if interaction.channel_id == elite_logs_channel_id:
                await self.add_to_queue(interaction, user, elite_queue)
            elif interaction.channel_id == premier_logs_channel_id:
                await self.add_to_queue(interaction, user, premier_queue)
            elif interaction.channel_id == championship_logs_channel_id:
                await self.add_to_queue(interaction, user, championship_queue)
            elif interaction.channel_id == casual_logs_channel_id:
                await self.add_to_queue(interaction, user, casual_queue)
            else:
                await interaction.response.send_message(
                    "Adding and removing players from the queue is not enabled in this channel."
                )

    async def add_to_queue(self, interaction, user, queue):
        queue.append(user.id)
        all_tier_queue.append(user.id)
        if len(queue) == 6:
            await interaction.response.send_message(f"Queue popped: {queue}")
        else:
            await interaction.response.send_message(f"{user.name} has joined the queue")
            print(elite_queue)
            print(premier_queue)
            print(championship_queue)
            print(casual_queue)
            print(all_tier_queue)


async def setup(bot):
    await bot.add_cog(queue_handler(bot))
