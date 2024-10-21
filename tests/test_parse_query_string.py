import unittest

from app.utils.parse_query_string import parse_query_string


class TestParseQueryString(unittest.TestCase):
    def test_valid_query_string(self):
        environ = {"QUERY_STRING": "playerId=1&gameId=2"}
        player_id, game_id = parse_query_string(environ)
        self.assertEqual(player_id, 1)
        self.assertEqual(game_id, 2)


if __name__ == "__main__":
    unittest.main()
