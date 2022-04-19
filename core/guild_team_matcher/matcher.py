import itertools

from guild_team_matcher.exceptions import PlayerNotFound
from guild_team_matcher.format import format_possible_teams
from guild_team_matcher.scrapper.guild_members import (
    filter_members_by_vocation,
    get_guild_members,
)
from guild_team_matcher.scrapper.player_info import requester_player_details
from guild_team_matcher.settings import GUILD_NAME


def match_team(player_name):
    """Function to calculate the possibilities of teams that can be formed with
    the informed player. The guild that will be used as base is defined by
    environment variable (GUILD_NAME).

    Args:
        player_name (str): Name of the player that will be used as a basis for
        team formation.

    Raises:
        PlayerNotFound: It is possible that the informed player does not exist.
        If this happens, this exception will be raised.

    Returns:
        str: Text with all teams formed, specifying player names, vocation and
        level.
    """
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


def calculate_team_formation_possibilities(flatted_guild_members_by_vocation):
    """We use a very simple logic to calculate the possibilities of teams:

    1 - We received as input a list of lists of all players divided by
    vocation.
    2 - Players with the same vocation as the player are not on this list.
    3 - To use the device, we need a list with only one element, which is
    precisely the base player for calculation.
    4 - We use `itertools.product` to generate all possible combinations with
    the vocation and player lists.
    5 - Once we have all the possibilities, we will iterate over each one and
    run a specific filter to see if all players in that specific formation
    share experience.
    6 - We return a list with only the combinations that share experience.

    An interesting point to emphasize is that all players on the team will
    necessarily have different vocations..

    Args:
        flatted_guild_members_by_vocation (list): List of player lists divided
        by vocation + list with base player.

    Returns:
        list: List of teams that can share experience with each other.
    """
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
    """Removes from the dictionary players who have the same vocation as the
    base player.

    Args:
        player (Player): Base player.
        guild_members_by_vocation (dict): Dictionary containing the lists of
        players divided by vocation.

    Returns:
        dict: Dictionary without players who have the same vocation as the
        base player.
    """
    vocation_to_skip = ""
    for vocation in guild_members_by_vocation.keys():
        if vocation in player.vocation:
            vocation_to_skip = vocation
            break

    del guild_members_by_vocation[vocation_to_skip]
    return guild_members_by_vocation


def flat_guild_members_by_vocation(guild_members):
    """Compress a dictionary containing players divided by vocation into a list
    of player lists by vocation.

    Args:
        guild_members (dict): Dictionary containing players divided by
        vocation.

    Returns:
        list: List of players list divided by vocation.
    """
    flatten_members = []
    for players_by_vocation in guild_members.values():
        flatten_members.append(players_by_vocation)

    return flatten_members


if __name__ == "__main__":
    print(match_team("Derfel"))
