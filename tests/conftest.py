import os


class MockRequests:
    def __init__(self, payload_file):
        with open(payload_file, "r") as fp:
            self.payload = fp.read()

    @property
    def text(self):
        return self.payload


def mocked_requests_player_info(*args, **kwargs):
    return MockRequests(
        os.path.join(os.getcwd(), "tests/static/player_info_page.html")
    )


def mocked_requests_player_not_found(*args, **kwargs):
    return MockRequests(
        os.path.join(os.getcwd(), "tests/static/non_existent_player_page.html")
    )
