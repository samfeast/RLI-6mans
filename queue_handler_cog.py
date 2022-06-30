from asyncore import write
import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import time

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

total = 0
random_vote = 0
captains_vote = 0
balanced_vote = 0


class queue_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping cog command
    @app_commands.command(description="Ping the elite cog.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def ping_queue_handler(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    # Queue command
    @app_commands.command(description="Join the queue.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def q(self, interaction: discord.Interaction):

        if interaction.user.id in all_tier_queue:
            await interaction.response.send_message(
                "Sorry! You are already in a 6mans queue.", ephemeral=True
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
                    "Queuing is not enabled in this channel.", ephemeral=True
                )

    # Add command
    @app_commands.command(description="Add a player to the queue.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def add(self, interaction: discord.Interaction, user: discord.User):

        if user.id in all_tier_queue:
            await interaction.response.send_message(
                "Sorry! This user is already in a 6mans queue.", ephemeral=True
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
                    "Adding and removing players from the queue is not enabled in this channel.",
                    ephemeral=True,
                )

    # Queue management and team generation function
    async def add_to_queue(self, interaction, user, raw_queue, channel_id, added):
        tier_channel = self.bot.get_channel(channel_id)
        raw_queue.append(user.id)
        all_tier_queue.append(user.id)
        if added:
            await interaction.response.send_message(
                f"{user.mention} has been added to the queue."
            )
            if len(raw_queue) == 1:
                embed = discord.Embed(title="1 player is in the queue!")
                embed.set_footer(
                    text="5 more needed!",
                    icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                )
            else:
                embed = discord.Embed(
                    title=f"{len(raw_queue)} players are in the queue!"
                )
                embed.set_footer(
                    text=f"{str(6-len(raw_queue))} more needed!",
                    icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                )
            embed.color = 0xFF8B00
            embed.description = f"{user.mention} has joined the queue."
            await tier_channel.send(embed=embed)
        else:

            if len(raw_queue) == 1:
                embed = discord.Embed(title=f"{len(raw_queue)} player is in the queue!")
                embed.set_footer(
                    text="5 more needed!",
                    icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                )
            else:
                embed = discord.Embed(
                    title=f"{len(raw_queue)} players are in the queue!"
                )
                embed.set_footer(
                    text=f"{str(6-len(raw_queue))} more needed!",
                    icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                )
            embed.color = 0xFF8B00
            embed.description = f"{user.mention} has joined the queue."
            await interaction.response.send_message(embed=embed)

        if len(raw_queue) == 6:

            queue = list(raw_queue)

            for player in queue:
                raw_queue.remove(player)

            for player in queue:
                all_tier_queue.remove(player)

            queue_reset = discord.Embed(title=f"Queue has been reset.", color=0xFF8B00)
            queue_reset.set_footer(
                text=f"When's the next one?...",
                icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
            )
            await tier_channel.send(embed=queue_reset)

            global voters
            voters = list(queue)

            view = team_picker()

            embed = discord.Embed(title="Choose game!", color=0xFFFFFF)
            embed.set_footer(
                text="Powered by RLI",
                icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
            )

            await tier_channel.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                print("Timed out...")
            elif view.value == "random":
                print("Teams will be generated randomly")
            elif view.value == "captains":
                print("Teams will be made by captains")
            elif view.value == "balanced":
                print("Teams will be balanced")

            random_queue = await self.random_teams(queue)

            with open("json/active_games.json", "r") as read_file:
                active_games = json.load(read_file)

            if channel_id == elite_channel_id:
                tier = "elite"
            elif channel_id == premier_channel_id:
                tier = "premier"
            elif channel_id == championship_channel_id:
                tier = "championship"
            if channel_id == casual_channel_id:
                tier = "casual"

            game_dict = {
                f"RLI{random.randint(1,1000)}": {
                    "timestamp": round(time.time()),
                    "tier": tier,
                    "team_1": random_queue[0],
                    "team_2": random_queue[1],
                }
            }

            active_games["active_games"].append(game_dict)

            with open("json/active_games.json", "w") as write_file:
                json.dump(active_games, write_file, indent=2)

            match_creator = random.choice(queue)

            teams_embed = discord.Embed(title=f"The Teams!", color=0x83FF00)
            teams_embed.add_field(
                name="**-Team 1-**",
                value=f"{self.bot.get_user(random_queue[0][0]).mention}, {self.bot.get_user(random_queue[0][1]).mention}, {self.bot.get_user(random_queue[0][2]).mention}",
                inline=False,
            )
            teams_embed.add_field(
                name="**-Team 2-**",
                value=f"{self.bot.get_user(random_queue[1][0]).mention}, {self.bot.get_user(random_queue[1][1]).mention}, {self.bot.get_user(random_queue[1][2]).mention}",
                inline=False,
            )
            teams_embed.add_field(
                name="**Match Creator:**",
                value=f"{self.bot.get_user(match_creator).mention}",
                inline=False,
            )
            teams_embed.set_footer(
                text=f"Powered by RLI",
                icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
            )
            await tier_channel.send(embed=teams_embed)

    # Leave command
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

    # Remove command
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

    # Queue removal function
    async def remove_from_queue(self, interaction, user, queue, channel_id, removed):
        tier_channel = self.bot.get_channel(channel_id)
        try:
            queue.remove(user.id)
            all_tier_queue.remove(user.id)
            if removed:
                await interaction.response.send_message(
                    f"{user.mention} has been removed from the queue."
                )
                if len(queue) == 1:
                    embed = discord.Embed(title="1 player is in the queue!")
                    embed.set_footer(
                        text="5 more needed!",
                        icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                    )
                else:
                    embed = discord.Embed(
                        title=f"{len(queue)} players are in the queue!"
                    )
                    embed.set_footer(
                        text=f"{str(6-len(queue))} more needed!",
                        icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                    )
                embed.color = 0xFFFFFF
                embed.description = f"{user.mention} has left the queue."
                await tier_channel.send(embed=embed)
            else:
                if len(queue) == 1:
                    embed = discord.Embed(title="1 player is in the queue!")
                    embed.set_footer(
                        text="5 more needed!",
                        icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                    )
                else:
                    embed = discord.Embed(
                        title=f"{len(queue)} players are in the queue!"
                    )
                    embed.set_footer(
                        text=f"{str(6-len(queue))} more needed!",
                        icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                    )
                embed.color = 0xFFFFFF
                embed.description = f"{user.mention} has left the queue."
                await interaction.response.send_message(embed=embed)
        except ValueError:
            if removed:
                await interaction.response.send_message("User is not in the queue.")
            else:
                await interaction.response.send_message(
                    "You are not currently in the queue."
                )

    # Random teams generator
    async def random_teams(self, queue):
        random.shuffle(queue)
        team1 = [queue[0], queue[1], queue[2]]
        team2 = [queue[3], queue[4], queue[5]]

        return team1, team2

    # Status command
    @app_commands.command(description="Check how many players are in the queue.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def status(self, interaction: discord.Interaction):
        if interaction.channel_id == elite_channel_id:
            await self.show_status(interaction, elite_queue)
        elif interaction.channel_id == premier_channel_id:
            await self.show_status(interaction, premier_queue)
        elif interaction.channel_id == championship_channel_id:
            await self.show_status(interaction, championship_queue)
        elif interaction.channel_id == casual_channel_id:
            await self.show_status(interaction, casual_queue)
        else:
            await interaction.response.send_message(
                "There is no queue in this channel.", ephemeral=True
            )

    async def show_status(self, interaction, queue):

        player_list = []
        for player in queue:
            player_list.append(self.bot.get_user(player).mention)

        embed = discord.Embed(title=f"{len(queue)} players are in the queue")
        embed.description = " ".join(player for player in player_list)
        embed.color = 0xFF8B00
        embed.set_footer(
            text=f"{str(6-len(queue))} more needed!",
            icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
        )
        await interaction.response.send_message(embed=embed)


class team_picker(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Random", style=discord.ButtonStyle.red)
    async def random(self, interaction: discord.Interaction, button: discord.ui.Button):
        global total
        global random_vote
        global captains_vote
        global balanced_vote
        await interaction.response.defer()

        if interaction.user.id in voters:
            voters.remove(interaction.user.id)
            total += 1
            random_vote += 1

            print("ran")
            print(total)
            if total == 6:
                if random_vote > captains_vote and random_vote > balanced_vote:
                    self.value = "random"
                    self.stop()
                if captains_vote > random_vote and captains_vote > balanced_vote:
                    self.value = "captains"
                    self.stop()
                if balanced_vote > captains_vote and balanced_vote > random_vote:
                    self.value = "balanced"
                    self.stop()

    @discord.ui.button(label="Captains", style=discord.ButtonStyle.blurple)
    async def captains(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        global total
        global random_vote
        global captains_vote
        global balanced_vote
        await interaction.response.defer()

        if interaction.user.id in voters:
            voters.remove(interaction.user.id)
            total += 1
            captains_vote += 1

            print("cap")
            print(total)
            if total == 6:
                if random_vote > captains_vote and random_vote > balanced_vote:
                    self.value = "random"
                    self.stop()
                if captains_vote > random_vote and captains_vote > balanced_vote:
                    self.value = "captains"
                    self.stop()
                if balanced_vote > captains_vote and balanced_vote > random_vote:
                    self.value = "balanced"
                    self.stop()

    @discord.ui.button(label="Balanced", style=discord.ButtonStyle.green)
    async def balanced(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        global total
        global random_vote
        global captains_vote
        global balanced_vote
        await interaction.response.defer()

        if interaction.user.id in voters:
            voters.remove(interaction.user.id)
            total += 1
            balanced_vote += 1

            print("bal")
            print(total)
            if total == 6:
                if random_vote > captains_vote and random_vote > balanced_vote:
                    self.value = "random"
                    self.stop()
                if captains_vote > random_vote and captains_vote > balanced_vote:
                    self.value = "captains"
                    self.stop()
                if balanced_vote > captains_vote and balanced_vote > random_vote:
                    self.value = "balanced"
                    self.stop()


async def setup(bot):
    await bot.add_cog(queue_handler(bot))
