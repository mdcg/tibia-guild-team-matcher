import sys
from guild_team_matcher.discord.bot import bot
from guild_team_matcher.settings import BOT_TOKEN


if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import (
        PackageNotFoundError,
        version,
    )  # pragma: no cover
else:
    from importlib_metadata import (
        PackageNotFoundError,
        version,
    )  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "guild-team-matcher"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


bot.run(BOT_TOKEN)
