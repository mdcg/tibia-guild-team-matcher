import pytest

from unittest import mock

from guild_team_matcher.scrapper.player_info import requester_player_details
from guild_team_matcher.scrapper.guild_members import (
    filter_members_by_vocation,
    get_guild_members,
)
from conftest import (
    mocked_requests_player_info,
    mocked_requests_player_not_found,
)


@mock.patch(
    "guild_team_matcher.scrapper.player_info.requests.get",
    side_effect=mocked_requests_player_info,
)
def test_requester_player_details(mock_requests):
    player = requester_player_details("Derfel")
    mock_requests.assert_called()
    assert player.name == "Derfel"
    assert player.level == 160
    assert player.vocation == "Elite Knight"


@mock.patch(
    "guild_team_matcher.scrapper.player_info.requests.get",
    side_effect=mocked_requests_player_not_found,
)
def test_requester_player_not_found(mock_requests):
    player = requester_player_details("a")
    mock_requests.assert_called()
    assert player is None
