from asyncore import write
import discord
from discord.ext import commands
from discord import app_commands
import json
import config

GUILD_ID = config.GUILD_ID


class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping cog command
    @app_commands.command(description="Ping the stats cog.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ping_stats(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    @app_commands.command(description="Show a players stats.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def stats(
        self,
        interaction: discord.Interaction,
        user: discord.User = None,
        manual_tier: str = None,
    ):

        if user == None:
            user = interaction.user

        with open("json/player_data.json", "r") as read_file:
            player_data = json.load(read_file)

        if manual_tier == None:
            if str(user.id) in player_data["elite"]:
                await self.show_stats(interaction, player_data, "elite", user)
            elif str(user.id) in player_data["premier"]:
                await self.show_stats(interaction, player_data, "premier", user)
            elif str(user.id) in player_data["championship"]:
                await self.show_stats(interaction, player_data, "championship", user)
            elif str(user.id) in player_data["casual"]:
                await self.show_stats(interaction, player_data, "casual", user)
            else:
                await interaction.response.send_message(
                    f"{user.name} has not played any games."
                )
        else:
            try:
                await self.show_stats(
                    interaction, player_data, manual_tier.lower(), user
                )
            except:
                await interaction.response.send_message("No stats found.")

    async def show_stats(self, interaction, player_data, tier, user):
        player_embed = discord.Embed(
            title=f"{user.name}'s {tier.capitalize()} Stats", color=user.color
        )

        player_embed.add_field(
            name="Games Played:",
            value=f"{player_data[tier][str(user.id)]['wins'] + player_data[tier][str(user.id)]['losses']}",
        )
        player_embed.add_field(
            name="Wins:", value=f"{player_data[tier][str(user.id)]['wins']}"
        )
        player_embed.add_field(
            name="Losses:", value=f"{player_data[tier][str(user.id)]['losses']}"
        )
        player_embed.add_field(
            name="Points:", value=f"{player_data[tier][str(user.id)]['points']:.2f}"
        )
        if (
            player_data[tier][str(user.id)]["wins"]
            + player_data[tier][str(user.id)]["losses"]
            == 0
        ):
            player_embed.add_field(name="Win Percentage:", value=f"0%")
            player_embed.add_field(name="Leaderboard Pos:", value="0/0")
        else:
            player_embed.add_field(
                name="Win Percentage:",
                value=f"{(player_data[tier][str(user.id)]['wins']/(player_data[tier][str(user.id)]['wins'] + player_data[tier][str(user.id)]['losses']))*100:.2f}%",
            )
            leaderboard_dict = {}
            for player in player_data[tier]:
                leaderboard_dict[player] = player_data[tier][player]["points"]

            i = 1

            for k, v in sorted(
                leaderboard_dict.items(), key=lambda item: item[1], reverse=True
            ):
                if k == str(user.id):
                    break

                i += 1

            player_embed.add_field(
                name="Leaderboard Pos:",
                value=f"{i}/{len(leaderboard_dict)}",
            )

        await interaction.response.send_message(embed=player_embed)

    @app_commands.command(description="Show the leaderboard.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def leaderboard(self, interaction: discord.Interaction, tier: str = None):
        with open("json/player_data.json", "r") as read_file:
            player_data = json.load(read_file)

        if tier == None:
            if str(interaction.user.id) in player_data["elite"]:
                await self.show_leaderboard(interaction, player_data, "elite", True)
            elif str(interaction.user.id) in player_data["premier"]:
                await self.show_leaderboard(interaction, player_data, "premier", True)
            elif str(interaction.user.id) in player_data["championship"]:
                await self.show_leaderboard(
                    interaction, player_data, "championship", True
                )
            elif str(interaction.user.id) in player_data["casual"]:
                await self.show_leaderboard(interaction, player_data, "casual", True)
            else:
                await interaction.response.send_message("Tier not found")
        else:
            try:
                await self.show_leaderboard(
                    interaction, player_data, tier.lower(), True
                )
            except:
                await interaction.response.send_message("Unable to display stats.")

    @app_commands.command(description="Show the reverse leaderboard.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def reverse_leaderboard(
        self, interaction: discord.Interaction, tier: str = None
    ):
        with open("json/player_data.json", "r") as read_file:
            player_data = json.load(read_file)

        if tier == None:
            if str(interaction.user.id) in player_data["elite"]:
                await self.show_leaderboard(interaction, player_data, "elite", False)
            elif str(interaction.user.id) in player_data["premier"]:
                await self.show_leaderboard(interaction, player_data, "premier", False)
            elif str(interaction.user.id) in player_data["championship"]:
                await self.show_leaderboard(
                    interaction, player_data, "championship", False
                )
            elif str(interaction.user.id) in player_data["casual"]:
                await self.show_leaderboard(interaction, player_data, "casual", False)
            else:
                await interaction.response.send_message("Tier not found")
        else:
            try:
                await self.show_leaderboard(
                    interaction, player_data, tier.lower(), False
                )
            except:
                await interaction.response.send_message("Unable to display stats.")

    async def show_leaderboard(self, interaction, player_data, tier, reverse):

        leaderboard_dict = {}
        for player in player_data[tier]:
            leaderboard_dict[player] = player_data[tier][player]["points"]

        leaderboard_embed = discord.Embed(
            title=f"{tier.capitalize()} Leaderboard", color=0x83FF00
        )
        i = 1

        if reverse == True:
            for k, v in sorted(
                leaderboard_dict.items(), key=lambda item: item[1], reverse=True
            ):
                leaderboard_embed.add_field(
                    name=f"{i}:",
                    value=f"{self.bot.get_user(int(k)).name}: {v:.2f}",
                    inline=False,
                )
                i += 1
        elif reverse == False:
            for k, v in sorted(
                leaderboard_dict.items(), key=lambda item: item[1], reverse=False
            ):
                leaderboard_embed.add_field(
                    name=f"{len(leaderboard_dict) + 1 - i}:",
                    value=f"{self.bot.get_user(int(k)).name}: {v:.2f}",
                    inline=False,
                )
                i += 1

        await interaction.response.send_message(embed=leaderboard_embed)


async def setup(bot):
    await bot.add_cog(stats(bot))
