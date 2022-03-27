import requests
from bs4 import BeautifulSoup
from guild_team_matcher.models import Player
from pydantic import ValidationError


def requester_player_details(player_name):
    """Performs data scraping in order to retrieve information from a specific
    player.

    Args:
        player_name (str): Player name.

    Returns:
        Player: Player instance with the information filled in. If the player
        cannot be found, None will be returned.
    """
    PLAYER_TABLE_INDEX = 0
    PLAYER_MAIN_TABLE_TR_INDEX = 0
    PROBABLE_FORMER_NAME_INDEX = 4
    PLAYER_VOCATION_INDEX = 9
    PLAYER_LEVEL_INDEX = 11

    # The player names in the query URL, if they have spaces, without
    # concatenated with +.
    formatted_player_name = "+".join(player_name.split(" "))
    player_details_url = (
        f"https://www.tibia.com/community/"
        f"?subtopic=characters&name={formatted_player_name}"
    )

    raw_player_details_html = requests.get(player_details_url).text

    soup = BeautifulSoup(raw_player_details_html, "html.parser")

    try:
        player_details_table = soup.find_all("table")[PLAYER_TABLE_INDEX]
        player_details_main_tr = player_details_table.find_all("tr")[
            PLAYER_MAIN_TABLE_TR_INDEX
        ]
        player_details_tds = player_details_main_tr.find_all("td")

        # It is interesting to check if the player has Former Names, if so, the
        # table structure changes and we will need to access different indices.
        if (
            player_details_tds[PROBABLE_FORMER_NAME_INDEX].text
            == "Former Names:"
        ):
            PLAYER_VOCATION_INDEX += 2
            PLAYER_LEVEL_INDEX += 2

        player_vocation = player_details_tds[PLAYER_VOCATION_INDEX].text
        player_level = player_details_tds[PLAYER_LEVEL_INDEX].text
    except (IndexError, KeyError, ValueError):
        return None

    try:
        player_info = Player(
            name=player_name,
            level=int(player_level),
            vocation=player_vocation,
            details=player_details_url,
        )
    except ValidationError:
        return None

    return player_info
