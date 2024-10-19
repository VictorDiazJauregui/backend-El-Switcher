import pytest

from app.db.db import GameStatus
from .db_setup import client, TestingSessionLocal, create_game, create_player


@pytest.fixture(scope="module")
def test_client():
    yield client


################# Test cases for /game/{game_id}/start #################


def test_start_game(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)
    create_player(db, game.id)
    create_player(db, game.id)

    # Now, start the game
    response = test_client.post(f"/game/{game.id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game.id
    assert data["status"] == GameStatus.INGAME.value


def test_start_full_game(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)
    create_player(db, game.id)
    create_player(db, game.id)

    # Now, start the game
    response = test_client.post(f"/game/{game.id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game.id
    assert data["status"] == GameStatus.INGAME.value


def test_start_full_game_4_players(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)
    create_player(db, game.id)
    create_player(db, game.id)
    create_player(db, game.id)
    create_player(db, game.id)

    # Now, start the game
    response = test_client.post(f"/game/{game.id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game.id
    assert data["status"] == GameStatus.INGAME.value


def test_start_already_started_game(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.INGAME)
    create_player(db, game.id)
    create_player(db, game.id)

    # Now, start the game
    response = test_client.post(f"/game/{game.id}/start")
    assert response.status_code == 400
    assert (
        response.json()["detail"] == f"Game {game.id} is already in progress."
    )


def test_not_enough_players(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)

    # Now, start the game
    response = test_client.post(f"/game/{game.id}/start")
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough players to start the game."


def test_start_nonexistent_game(test_client):
    """Test starting a non-existent game"""
    nonexistent_game_id = 999  # Assuming this game ID does not exist
    response = test_client.post(f"/game/{nonexistent_game_id}/start")

    # The expected response should be 404 Not Found
    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == f"Game with id {nonexistent_game_id} does not exist."
    )
