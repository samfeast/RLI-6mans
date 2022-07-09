from asyncore import write
import discord
from discord.ext import commands
from discord import app_commands
import json
import config

GUILD_ID = config.GUILD_ID


class reporting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping cog command
    @app_commands.command(description="Ping the reporting cog.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ping_reporting(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    @app_commands.command(description="Report a win.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def win(self, interaction: discord.Interaction, id: str):
        with open("json/active_games.json", "r") as read_file:
            active_games = json.load(read_file)

        for game in active_games["active_games"]:
            if game["id"].lower() == id.lower():
                game_dict = game
                break
            else:
                game_dict = None

        if interaction.user.id in game["team_1"]:
            await self.log_game(game_dict, game["team_1"], game["team_2"])
            await self.log_player_data(game_dict, game["team_1"], game["team_2"])

            winning_players = []
            losing_players = []
            for player in game["team_1"]:
                winning_players.append(self.bot.get_user(player).name)
            for player in game["team_2"]:
                losing_players.append(self.bot.get_user(player).name)

            embed = discord.Embed(
                title=f"{game_dict['tier'].capitalize()} Game: {game_dict['id']}",
                color=0x83FF00,
            )
            embed.add_field(
                name="Winning Team",
                value=" ".join(player for player in winning_players),
                inline=False,
            )
            embed.add_field(
                name="Losing Team",
                value=" ".join(player for player in losing_players),
                inline=False,
            )
            embed.set_footer(
                text=f"Powered by RLI, for RLI",
                icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
            )
            await interaction.response.send_message(embed=embed)

            active_games["active_games"].remove(game_dict)

        elif interaction.user.id in game["team_2"]:
            await self.log_game(game_dict, game["team_2"], game["team_1"])
            await self.log_player_data(game_dict, game["team_2"], game["team_1"])

            winning_players = []
            losing_players = []
            for player in game["team_2"]:
                winning_players.append(self.bot.get_user(player).name)
            for player in game["team_1"]:
                losing_players.append(self.bot.get_user(player).name)

            embed = discord.Embed(
                title=f"{game_dict['tier'].capitalize()} Game: {game_dict['id']}",
                color=0x83FF00,
            )
            embed.add_field(
                name="Winning Team",
                value=" ".join(player for player in winning_players),
                inline=False,
            )
            embed.add_field(
                name="Losing Team",
                value=" ".join(player for player in losing_players),
                inline=False,
            )
            embed.set_footer(
                text=f"Powered by RLI, for RLI",
                icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
            )
            await interaction.response.send_message(embed=embed)

            active_games["active_games"].remove(game_dict)

        else:
            await interaction.response.send_message(
                "You do not have permission to report this result."
            )

        with open("json/active_games.json", "w") as write_file:
            json.dump(active_games, write_file, indent=2)

    async def log_game(self, dict, winner, loser):
        with open("json/game_log.json", "r") as read_file:
            game_log = json.load(read_file)

        new_dict = {
            "id": dict["id"],
            "timestamp": dict["timestamp"],
            "tier": dict["tier"],
            "winning_players": winner,
            "losing_players": loser,
        }

        game_log["game_log"].append(new_dict)

        with open("json/game_log.json", "w") as write_file:
            json.dump(game_log, write_file, indent=2)

    async def log_player_data(self, dict, winner, loser):
        with open("json/player_data.json", "r") as read_file:
            player_data = json.load(read_file)

        for player in winner:
            id = str(player)
            if id in player_data[dict["tier"]]:
                player_data[dict["tier"]][id]["wins"] += 1
                player_data[dict["tier"]][id]["points"] += 1.42
            else:
                player_data[dict["tier"]][id] = {
                    "wins": 1,
                    "losses": 0,
                    "points": 1.42,
                    "elo": 1000,
                }

        for player in loser:
            id = str(player)
            if id in player_data[dict["tier"]]:
                player_data[dict["tier"]][id]["losses"] += 1
                player_data[dict["tier"]][id]["points"] -= 1
            else:
                player_data[dict["tier"]][id] = {
                    "losses": 1,
                    "wins": 0,
                    "points": -1,
                    "elo": 1000,
                }

        gain = 20

        for player in winner:
            current_elo = player_data[dict["tier"]][str(player)]["elo"]

            if winner == dict["team_1"]:
                new_elo = current_elo + (gain * (1 - dict["p1_win"]))
            else:
                new_elo = current_elo + (gain * (1 - dict["p2_win"]))
            print(f"{player}: {current_elo} -> {new_elo}")
            player_data[dict["tier"]][str(player)]["elo"] = new_elo

        for player in loser:
            current_elo = player_data[dict["tier"]][str(player)]["elo"]

            if loser == dict["team_1"]:
                new_elo = current_elo + (gain * (0 - dict["p1_win"]))
            else:
                new_elo = current_elo + (gain * (0 - dict["p2_win"]))
            print(f"{player}: {current_elo} -> {new_elo}")
            player_data[dict["tier"]][str(player)]["elo"] = new_elo

        with open("json/player_data.json", "w") as write_file:
            json.dump(player_data, write_file, indent=2)


async def setup(bot):
    await bot.add_cog(reporting(bot))
