import pytest
from app.db.db import GameStatus, Turn
from .db_setup import client, TestingSessionLocal, create_game, create_player


@pytest.fixture(scope="module")
def test_client():
    yield client


def test_end_turn_success():
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.INGAME)
    player = create_player(db, game.id)

    response = client.post(f"/game/{game.id}/end_turn/{player.id}")
    assert response.status_code == 200

    assert response.json() == {
        "message": "Player test_player has ended their turn."
    }


def test_end_turn_invalid_game_id():
    response = client.post("/game/999/end_turn/1")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Game with id 999 does not exist."}


def test_end_turn_invalid_player_id():
    response = client.post("/game/1/end_turn/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Player with id 999 does not exist."}


def test_end_turn_not_player_turn():
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.INGAME)
    player = create_player(db, game.id)
    player.turn = Turn.P2
    db.commit()
    db.refresh(player)

    response = client.post(f"/game/{game.id}/end_turn/{player.id}")
    assert response.status_code == 400
    assert response.json() == {"detail": f"It's not {player.id} turn."}


def test_end_turn_game_not_started():
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)
    player = create_player(db, game.id)

    response = client.post(f"/game/{game.id}/end_turn/{player.id}")
    assert response.status_code == 400
    assert response.json() == {"detail": f"Game {game.id} is not in progress."}
