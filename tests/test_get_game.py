import pytest
from app.db.db import GameStatus
from .db_setup import client, TestingSessionLocal, create_game


@pytest.fixture(scope="module")
def test_client():
    yield client


def test_get_game_by_id():

    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY)

    response = client.get(f"/game/{game.id}")

    assert response.status_code == 200
    assert response.json() == {
        "gameId": game.id,
        "gameName": game.name,
        "maxPlayers": game.max_players,
        "minPlayers": game.min_players,
        "status": game.status.value,
    }
