from asyncore import write
import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import time
import asyncio

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

elite_queue = [
    495542213535858693,
    297085754658652172,
    142700274849415170,
    415174814534467584,
    402523329954840596,
]
premier_queue = []
championship_queue = []
casual_queue = []

all_tier_queue = [
    495542213535858693,
    297085754658652172,
    142700274849415170,
    415174814534467584,
    402523329954840596,
]


class queue_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping cog command
    @app_commands.command(description="Ping the queue handler cog.")
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

            global total
            global random_vote
            global captains_vote
            global balanced_vote
            total = 5
            random_vote = 2
            captains_vote = 2
            balanced_vote = 1

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
                set_queue = await self.random_teams(queue)
            elif view.value == "random":
                set_queue = await self.random_teams(queue)
            elif view.value == "captains":
                set_queue = await self.captains_teams(queue, channel_id)
            elif view.value == "balanced":
                print("Teams will be balanced")

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

            game_id = random.randint(1, 1000)

            game_dict = {
                "id": f"RLI{game_id}",
                "timestamp": round(time.time()),
                "tier": tier,
                "team_1": set_queue[0],
                "team_2": set_queue[1],
            }

            active_games["active_games"].append(game_dict)

            with open("json/active_games.json", "w") as write_file:
                json.dump(active_games, write_file, indent=2)

            match_creator = random.choice(queue)

            teams_embed = discord.Embed(title=f"The Teams!", color=0x83FF00)
            teams_embed.add_field(
                name="**-Team 1-**",
                value=f"{self.bot.get_user(set_queue[0][0]).mention}, {self.bot.get_user(set_queue[0][1]).mention}, {self.bot.get_user(set_queue[0][2]).mention}",
                inline=False,
            )
            teams_embed.add_field(
                name="**-Team 2-**",
                value=f"{self.bot.get_user(set_queue[1][0]).mention}, {self.bot.get_user(set_queue[1][1]).mention}, {self.bot.get_user(set_queue[1][2]).mention}",
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

            private_teams_embed = discord.Embed(title=f"The Teams!", color=0x83FF00)
            private_teams_embed.add_field(
                name="**-Team 1-**",
                value=f"{self.bot.get_user(set_queue[0][0]).mention}, {self.bot.get_user(set_queue[0][1]).mention}, {self.bot.get_user(set_queue[0][2]).mention}",
                inline=False,
            )
            private_teams_embed.add_field(
                name="**-Team 2-**",
                value=f"{self.bot.get_user(set_queue[1][0]).mention}, {self.bot.get_user(set_queue[1][1]).mention}, {self.bot.get_user(set_queue[1][2]).mention}",
                inline=False,
            )
            private_teams_embed.add_field(
                name="**Match Creator:**",
                value=f"{self.bot.get_user(match_creator).mention}",
                inline=False,
            )

            password = f"RLI{random.randint(1, 1000)}"

            private_teams_embed.add_field(
                name="**Username:**", value=game_id, inline=True
            )
            private_teams_embed.add_field(
                name="**Password:**", value=password, inline=True
            )

            for player in set_queue[0]:
                try:
                    player_object = self.bot.get_user(player)
                    # await player_object.send(embed=private_teams_embed)
                    await player_object.send(
                        "Sorry again! Please disregard these messages. You may want to mute me as there will probably be quite a few more to come."
                    )
                except:
                    print(f"Could not dm {player}")
            for player in set_queue[1]:
                try:
                    player_object = self.bot.get_user(player)
                    # await player_object.send(embed=private_teams_embed)
                    await player_object.send(
                        "Sorry again! Please disregard these messages. You may want to mute me as there will probably be quite a few more to come."
                    )
                except:
                    print(f"Could not dm {player}")

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

    async def captains_teams(self, queue, channel_id):

        with open("json/player_data.json", "r") as read_file:
            player_data = json.load(read_file)

        if channel_id == elite_channel_id:
            tier = "elite"
        elif channel_id == premier_channel_id:
            tier = "premier"
        elif channel_id == championship_channel_id:
            tier = "championship"
        elif channel_id == casual_channel_id:
            tier = "casual"

        tier_channel = self.bot.get_channel(channel_id)

        player_data_dict = {}
        for player in queue:
            try:
                player_data_dict[str(player)] = player_data[tier][str(player)]["points"]
            except KeyError:
                player_data_dict[str(player)] = 0

        i = 0
        ordered_players = []
        for k, v in sorted(
            player_data_dict.items(), key=lambda item: item[1], reverse=True
        ):
            ordered_players.append(k)
            i += 1

        captain1 = int(ordered_players[0])
        captain2 = int(ordered_players[1])
        ordered_players.remove(str(captain1))
        ordered_players.remove(str(captain2))

        team1 = [captain1]
        team2 = [captain2]

        global allowed_to_pick
        allowed_to_pick = str(captain1)

        view = first_pick()

        embed = discord.Embed(title="Pick your teams!", color=0x0099FF)
        embed.add_field(
            name="Team 1", value=self.bot.get_user(captain1).name, inline=True
        )
        embed.add_field(
            name="Team 2", value=self.bot.get_user(captain2).name, inline=True
        )
        embed.add_field(
            name="Player 1",
            value=self.bot.get_user(int(ordered_players[0])).name,
            inline=False,
        )
        embed.add_field(
            name="Player 2",
            value=self.bot.get_user(int(ordered_players[1])).name,
            inline=False,
        )
        embed.add_field(
            name="Player 3",
            value=self.bot.get_user(int(ordered_players[2])).name,
            inline=False,
        )
        embed.add_field(
            name="Player 4",
            value=self.bot.get_user(int(ordered_players[3])).name,
            inline=False,
        )
        embed.set_footer(
            text=f"{self.bot.get_user(int(allowed_to_pick)).name}'s turn to choose",
            icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
        )
        embed.set_thumbnail(url=self.bot.get_user(int(allowed_to_pick)).avatar.url)
        first_pick_embed = await tier_channel.send(embed=embed, view=view)

        await view.wait()
        first_player_pick = ordered_players[view.value]
        team1.append(int(first_player_pick))
        ordered_players.remove(first_player_pick)
        await first_pick_embed.delete()

        allowed_to_pick = str(captain2)
        view = second_pick()

        embed = discord.Embed(title="Pick your teams!", color=0x0099FF)
        embed.add_field(
            name="Team 1",
            value=f"{self.bot.get_user(captain1).name}, {self.bot.get_user(team1[1]).name}",
            inline=True,
        )
        embed.add_field(
            name="Team 2", value=f"{self.bot.get_user(captain2).name}", inline=True
        )
        embed.add_field(
            name="Player 1",
            value=self.bot.get_user(int(ordered_players[0])).name,
            inline=False,
        )
        embed.add_field(
            name="Player 2",
            value=self.bot.get_user(int(ordered_players[1])).name,
            inline=False,
        )
        embed.add_field(
            name="Player 3",
            value=self.bot.get_user(int(ordered_players[2])).name,
            inline=False,
        )
        embed.set_thumbnail(url=self.bot.get_user(int(allowed_to_pick)).avatar.url)
        embed.set_footer(
            text=f"{self.bot.get_user(int(allowed_to_pick)).name}'s turn to choose",
            icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
        )
        second_pick_embed = await tier_channel.send(embed=embed, view=view)

        await view.wait()
        second_player_pick = ordered_players[view.value]
        team2.append(int(second_player_pick))
        ordered_players.remove(second_player_pick)
        await second_pick_embed.delete()

        view = third_pick()

        embed = discord.Embed(title="Pick your teams!", color=0x0099FF)
        embed.add_field(
            name="Team 1",
            value=f"{self.bot.get_user(captain1).name}, {self.bot.get_user(team1[1]).name}",
            inline=True,
        )
        embed.add_field(
            name="Team 2",
            value=f"{self.bot.get_user(captain2).name}, {self.bot.get_user(team2[1]).name}",
            inline=True,
        )
        embed.add_field(
            name="Player 1",
            value=self.bot.get_user(int(ordered_players[0])).name,
            inline=False,
        )
        embed.add_field(
            name="Player 2",
            value=self.bot.get_user(int(ordered_players[1])).name,
            inline=False,
        )
        embed.set_thumbnail(url=self.bot.get_user(int(allowed_to_pick)).avatar.url)
        embed.set_footer(
            text=f"{self.bot.get_user(int(allowed_to_pick)).name}'s turn to choose",
            icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
        )
        third_pick_embed = await tier_channel.send(embed=embed, view=view)

        await view.wait()
        third_player_pick = ordered_players[view.value]
        team2.append(int(third_player_pick))
        ordered_players.remove(third_player_pick)
        await third_pick_embed.delete()

        team1.append(int(ordered_players[0]))

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

            if random_vote == 4:
                self.value = "random"
                self.stop()
            else:
                if total == 6:
                    if random_vote > captains_vote and random_vote > balanced_vote:
                        self.value = "random"
                        self.stop()
                    elif captains_vote > random_vote and captains_vote > balanced_vote:
                        self.value = "captains"
                        self.stop()
                    elif balanced_vote > captains_vote and balanced_vote > random_vote:
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

            if captains_vote == 4:
                self.value = "captains"
                self.stop()
            else:
                if total == 6:
                    if random_vote > captains_vote and random_vote > balanced_vote:
                        self.value = "random"
                        self.stop()
                    elif captains_vote > random_vote and captains_vote > balanced_vote:
                        self.value = "captains"
                        self.stop()
                    elif balanced_vote > captains_vote and balanced_vote > random_vote:
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

            if balanced_vote == 4:
                self.value = "balanced"
                self.stop()
            else:
                if total == 6:
                    if random_vote > captains_vote and random_vote > balanced_vote:
                        self.value = "random"
                        self.stop()
                    elif captains_vote > random_vote and captains_vote > balanced_vote:
                        self.value = "captains"
                        self.stop()
                    elif balanced_vote > captains_vote and balanced_vote > random_vote:
                        self.value = "balanced"
                        self.stop()
                    elif random_vote == captains_vote == balanced_vote:
                        self.value = "random"
                        self.stop()


class first_pick(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="1", style=discord.ButtonStyle.blurple)
    async def pick_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 0
            self.stop()

    @discord.ui.button(label="2", style=discord.ButtonStyle.blurple)
    async def pick_2(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 1
            self.stop()

    @discord.ui.button(label="3", style=discord.ButtonStyle.blurple)
    async def pick_3(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 2
            self.stop()

    @discord.ui.button(label="4", style=discord.ButtonStyle.blurple)
    async def pick_4(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 3
            self.stop()


class second_pick(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="1", style=discord.ButtonStyle.blurple)
    async def pick_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 0
            self.stop()

    @discord.ui.button(label="2", style=discord.ButtonStyle.blurple)
    async def pick_2(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 1
            self.stop()

    @discord.ui.button(label="3", style=discord.ButtonStyle.blurple)
    async def pick_3(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 2
            self.stop()


class third_pick(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="1", style=discord.ButtonStyle.blurple)
    async def pick_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 0
            self.stop()

    @discord.ui.button(label="2", style=discord.ButtonStyle.blurple)
    async def pick_2(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        global allowed_to_pick
        if str(interaction.user.id) == allowed_to_pick:
            self.value = 1
            self.stop()


async def setup(bot):
    await bot.add_cog(queue_handler(bot))
