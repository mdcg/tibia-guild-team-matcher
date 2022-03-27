import requests
from bs4 import BeautifulSoup
from core.guild_team_matcher.models import Player
from pydantic import ValidationError


def requester_player_details(player_name):
    PLAYER_TABLE_INDEX = 0
    PLAYER_VOCATION_TR_INDEX = 5
    PLAYER_VOCATION_TD_INDEX = 1
    PLAYER_LEVEL_TR_INDEX = 6
    PLAYER_LEVEL_TD_INDEX = 1

    # O nomes dos jogadores na URL de consulta, caso tenham espaco, sem concatenados com +.
    formatted_player_name = "+".join(player_name.split(" "))
    player_details_url = (
        f"https://www.tibia.com/community/"
        f"?subtopic=characters&name={formatted_player_name}"
    )

    raw_player_details_html = requests.get(player_details_url).text

    soup = BeautifulSoup(raw_player_details_html, "html.parser")

    try:
        player_details_table = soup.find_all("table")[PLAYER_TABLE_INDEX]
        player_details_trs = player_details_table.find_all("tr")

        player_vocation = (
            player_details_trs[PLAYER_VOCATION_TR_INDEX]
            .find_all("td")[PLAYER_VOCATION_TD_INDEX]
            .text
        )
        player_level = (
            player_details_trs[PLAYER_LEVEL_TR_INDEX]
            .find_all("td")[PLAYER_LEVEL_TD_INDEX]
            .text
        )
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


if __name__ == "__main__":
    requester_player_details("Sux")
