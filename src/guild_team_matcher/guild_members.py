import requests
from bs4 import BeautifulSoup


def get_guild_members(guild_name):
    GUILD_TABLE_INDEX = 6
    raw_guild_details_html = requests.post("https://www.tibia.com/community/?subtopic=guilds&page=view", data={"GuildName": guild_name}).text
    soup = BeautifulSoup(raw_guild_details_html, 'html.parser')
    members_table = soup.find_all("table")[GUILD_TABLE_INDEX]
    return members_table


def filter_members_by_vocation(guild_members):
    members_peer_vocation = {
        "Sorcerer": [],
        "Druid": [],
        "Knight": [],
        "Paladin": [], 
    }
    SKIP_HEADER_TR = 1
    for member_info_tr in guild_members.find_all("tr"):
        member_info_tds = member_info_tr.find_all("td")
        try:
            member = {
                "name": member_info_tds[1].text,
                "details": member_info_tds[1].a["href"],
                "vocation": member_info_tds[2].text,
                "level": member_info_tds[3].text,
            }
        except (IndexError, AttributeError, TypeError):
            continue

        for vocation in members_peer_vocation.keys():
            if vocation in member["vocation"]:
                members_peer_vocation[vocation].append(member)
    
    return members_peer_vocation


if __name__ == "__main__":
    members = get_guild_members("Sucesso")
    for ms in filter_members_by_vocation(members)["Druid"]:
        print(f"{ms['name']} ({ms['level']}) - {ms['details']}")
