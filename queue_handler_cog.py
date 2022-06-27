import discord
from discord.ext import commands
from discord import app_commands
import json
import random

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
premier_queue = [
    297085754658652172,
    495542213535858693,
    209776204817891328,
    202118945803730944,
    201478097667751936,
]
championship_queue = []
casual_queue = []

all_tier_queue = [
    297085754658652172,
    495542213535858693,
    209776204817891328,
    202118945803730944,
    201478097667751936,
]


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
                await self.add_to_queue(
                    interaction, interaction.user, elite_queue, elite_channel_id, False
                )
            elif interaction.channel_id == premier_channel_id:
                await self.add_to_queue(
                    interaction,
                    interaction.user,
                    premier_queue,
                    premier_channel_id,
                    False,
                )
            elif interaction.channel_id == championship_channel_id:
                await self.add_to_queue(
                    interaction,
                    interaction.user,
                    championship_queue,
                    championship_channel_id,
                    False,
                )
            elif interaction.channel_id == casual_channel_id:
                await self.add_to_queue(
                    interaction,
                    interaction.user,
                    casual_queue,
                    casual_channel_id,
                    False,
                )
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
                await self.add_to_queue(
                    interaction, user, elite_queue, elite_channel_id, True
                )
            elif interaction.channel_id == premier_logs_channel_id:
                await self.add_to_queue(
                    interaction, user, premier_queue, premier_channel_id, True
                )
            elif interaction.channel_id == championship_logs_channel_id:
                await self.add_to_queue(
                    interaction, user, championship_queue, championship_channel_id, True
                )
            elif interaction.channel_id == casual_logs_channel_id:
                await self.add_to_queue(
                    interaction, user, casual_queue, casual_channel_id, True
                )
            else:
                await interaction.response.send_message(
                    "Adding and removing players from the queue is not enabled in this channel."
                )

    async def add_to_queue(self, interaction, user, queue, channel_id, added):
        tier_channel = self.bot.get_channel(channel_id)
        queue.append(user.id)
        all_tier_queue.append(user.id)
        if added:
            await interaction.response.send_message(f"{user.name} added to queue.")
            await tier_channel.send(f"{user.name} has joined the queue.")
        else:
            await interaction.response.send_message(
                f"{user.name} has joined the queue."
            )
        if len(queue) == 6:
            await tier_channel.send(f"Queue popped: {queue}")
            random_queue = await self.random_teams(queue)
            print(random_queue)
            await tier_channel.send(f"Teams: {random_queue}")

    @app_commands.command(description="Leave the queue.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def l(self, interaction: discord.Interaction):
        if interaction.channel_id == elite_channel_id:
            await self.remove_from_queue(
                interaction, interaction.user, elite_queue, elite_channel_id, False
            )
        elif interaction.channel_id == premier_channel_id:
            await self.remove_from_queue(
                interaction, interaction.user, premier_queue, premier_channel_id, False
            )
        elif interaction.channel_id == championship_channel_id:
            await self.remove_from_queue(
                interaction,
                interaction.user,
                championship_queue,
                championship_channel_id,
                False,
            )
        elif interaction.channel_id == casual_channel_id:
            await self.remove_from_queue(
                interaction, interaction.user, casual_queue, casual_channel_id, False
            )
        else:
            await interaction.response.send_message(
                "Queuing is not enabled in this channel."
            )

    @app_commands.command(description="Remove a player from the queue.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def remove(self, interaction: discord.Interaction, user: discord.User):
        if interaction.channel_id == elite_logs_channel_id:
            await self.remove_from_queue(
                interaction, user, elite_queue, elite_channel_id, True
            )
        elif interaction.channel_id == premier_logs_channel_id:
            await self.remove_from_queue(
                interaction, user, premier_queue, premier_channel_id, True
            )
        elif interaction.channel_id == championship_logs_channel_id:
            await self.remove_from_queue(
                interaction, user, championship_queue, championship_channel_id, True
            )
        elif interaction.channel_id == casual_logs_channel_id:
            await self.remove_from_queue(
                interaction, user, casual_queue, casual_channel_id, True
            )
        else:
            await interaction.response.send_message(
                "Adding and removing players from the queue is not enabled in this channel."
            )

    async def remove_from_queue(self, interaction, user, queue, channel_id, removed):
        tier_channel = self.bot.get_channel(channel_id)
        try:
            queue.remove(user.id)
            all_tier_queue.remove(user.id)
            if removed:
                await interaction.response.send_message(
                    f"{user.name} has been removed from the queue."
                )
                await tier_channel.send(f"{user.name} has left the queue.")
            else:
                await interaction.response.send_message(
                    f"{user.name} has left the queue."
                )
        except ValueError:
            if removed:
                await interaction.response.send_message("User is not in the queue.")
            else:
                await interaction.response.send_message("You are not in the queue.")

    async def random_teams(self, queue):
        print(queue)
        random.shuffle(queue)
        print(queue)
        team1 = [queue[0], queue[1], queue[2]]
        team2 = [queue[3], queue[4], queue[5]]

        return team1, team2


async def setup(bot):
    await bot.add_cog(queue_handler(bot))
