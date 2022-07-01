from asyncore import write
import discord
from discord.ext import commands
from discord import app_commands
import json


class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping cog command
    @app_commands.command(description="Ping the stats cog.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def ping_stats(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    @app_commands.command(description="Show a players stats.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def stats(
        self,
        interaction: discord.Interaction,
        user: discord.User = None,
        manual_tier: str = None,
    ):

        if user == None:
            user = interaction.user

        print(user.id)

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
            player_embed.add_field(name="Leaderboard Pos:", value=f"x/x")

        await interaction.response.send_message(embed=player_embed)


async def setup(bot):
    await bot.add_cog(stats(bot))
