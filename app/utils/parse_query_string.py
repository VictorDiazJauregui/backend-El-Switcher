import urllib


def parse_query_string(environ):
    query_string = environ.get("QUERY_STRING", "")
    parsed_qs = urllib.parse.parse_qs(query_string)

    return int(parsed_qs.get("playerId")[0]), int(parsed_qs.get("gameId")[0])
