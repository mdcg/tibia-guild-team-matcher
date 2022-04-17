from guild_team_matcher.logs import logger
from guild_team_matcher.settings import BOT_TOKEN

import discord
from discord.ext import commands

DESCRIPTION = """
Tibia Guild Team Matcher!

Developed by Sucesso!
"""

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    description=DESCRIPTION,
)


@bot.event
async def on_ready():
    """Simple event to know that the bot is ready to be invoked."""
    logger.info(f"Logged in as {bot.user.name} - {bot.user.id}")


@bot.command()
async def match(ctx, player_name: str):
    """Command to form all the possibilities of teams that can be formed from
    the name of the player informed. Teams will be formed from the members of
    the guild that is configured in the bot.

    Args:
        ctx (discord.ext.commands.Context): Represents the context in which a
        command is being invoked under.
        player_name (str): Player name that will be used as a basis to generate
        team formation possibilities.
    """
    if not player_name.isalpha():
        await ctx.send("Nome de jogar inválido. Tente novamente.")
        return None


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
