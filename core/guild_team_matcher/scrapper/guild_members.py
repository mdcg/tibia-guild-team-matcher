from guild_team_matcher.models import Player

import requests
from bs4 import BeautifulSoup
from pydantic import ValidationError


def get_guild_members(guild_name):
    """Simple data scraping on the Guild page informed by the parameter.

    Args:
        guild_name (str): Guild name.

    Returns:
        bs4.element.Tag: Object with all items in the table referring to Guild
        member data.
    """
    GUILD_TABLE_INDEX = 6

    raw_guild_details_html = requests.post(
        "https://www.tibia.com/community/?subtopic=guilds&page=view",
        data={"GuildName": guild_name},
    ).text

    soup = BeautifulSoup(raw_guild_details_html, "html.parser")
    members_table = soup.find_all("table")[GUILD_TABLE_INDEX]

    return members_table


def filter_members_by_vocation(guild_members):
    """Filters guild members by separating them into their respective
    vocations. To facilitate future consultations, we have separated some
    information by member: Name, Level and details (link about the char in
    Tibia).

    Args:
        guild_members (bs4.element.Tag): Information about guild members is
        contained in a table on the Tibia website. Basically, this parameter is
        just this table.

    Returns:
        dict: Dictionary where keys are Tibia vocations and values ​​are list
        of members belonging to specific vocation.
    """
    SKIP_HEADER_TR = 1

    members_peer_vocation = {
        "Sorcerer": [],
        "Druid": [],
        "Knight": [],
        "Paladin": [],
    }

    for member_info_tr in guild_members.find_all("tr"):
        member_info_tds = member_info_tr.find_all("td")
        try:
            member = Player(
                name=member_info_tds[1].text,
                level=int(member_info_tds[3].text),
                details=member_info_tds[1].a["href"],
                vocation=member_info_tds[2].text,
            )
        except (
            AttributeError,
            IndexError,
            TypeError,
            ValidationError,
            ValueError,
        ):
            continue

        for vocation in members_peer_vocation.keys():
            if vocation in member.vocation:
                members_peer_vocation[vocation].append(member)

    return members_peer_vocation


if __name__ == "__main__":
    print(filter_members_by_vocation(get_guild_members("Sucesso")))
