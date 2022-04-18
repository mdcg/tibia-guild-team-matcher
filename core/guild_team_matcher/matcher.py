import itertools

from guild_team_matcher.scrapper.player_info import requester_player_details
from guild_team_matcher.scrapper.guild_members import (
    filter_members_by_vocation,
    get_guild_members,
)
from guild_team_matcher.settings import GUILD_NAME
from guild_team_matcher.exceptions import PlayerNotFound


def match_team(player_name):
    player = requester_player_details(player_name)
    if player is None:
        raise PlayerNotFound(f"There is no player named {player_name}")

    guild_members_by_vocation = filter_members_by_vocation(
        get_guild_members(GUILD_NAME)
    )
    guild_members_without_same_player_vocation = (
        remove_guild_members_with_players_same_vocation(
            player, guild_members_by_vocation
        )
    )
    flatted_guild_members_by_vocation = flat_guild_members_by_vocation(
        guild_members_without_same_player_vocation
    )
    flatted_guild_members_by_vocation.append([player])
    possible_teams = calculate_team_formation_possibilities(
        flatted_guild_members_by_vocation
    )

    return format_possible_teams(possible_teams)


def format_possible_teams(possible_teams):
    possible_teams_text = ""
    for members in possible_teams:
        possible_teams_text += " | ".join([str(p) for p in members])
        possible_teams_text += "\n"

    return possible_teams_text


def calculate_team_formation_possibilities(flatted_guild_members_by_vocation):
    combinated_players_possibilities = itertools.product(
        *flatted_guild_members_by_vocation
    )
    LOWEST_PLAYER_LEVEL_INDEX = 0
    HIGHEST_PLAYER_LEVEL_INDEX = 3
    matched_team = []
    for possible_team in list(combinated_players_possibilities):
        sorted_members_by_level = sorted(possible_team, key=lambda p: p.level)
        if (
            sorted_members_by_level[HIGHEST_PLAYER_LEVEL_INDEX].level * (2 / 3)
            < sorted_members_by_level[LOWEST_PLAYER_LEVEL_INDEX].level
        ):
            matched_team.append(sorted_members_by_level)

    return matched_team


def remove_guild_members_with_players_same_vocation(
    player, guild_members_by_vocation
):
    vocation_to_skip = ""
    for vocation in guild_members_by_vocation.keys():
        if vocation in player.vocation:
            vocation_to_skip = vocation
            break

    del guild_members_by_vocation[vocation_to_skip]
    return guild_members_by_vocation


def flat_guild_members_by_vocation(guild_members):
    flatten_members = []
    for players_by_vocation in guild_members.values():
        flatten_members.append(players_by_vocation)

    return flatten_members


if __name__ == "__main__":
    print(match_team("Derfel"))
