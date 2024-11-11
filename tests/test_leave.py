import pytest
from app.db.db import GameStatus
from .db_setup import (
    client,
    TestingSessionLocal,
    create_game,
    create_player,
)


@pytest.fixture(scope="module")
def test_client():
    yield client


def test_leave_lobby(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.INGAME)
    player = create_player(db, game.id)

    # Delete player from the lobby
    response = test_client.delete(f"/game/{game.id}/leave/{player.id}")
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == f"""Player {player.name} has left the game."""
    )


def test_leave_lobby_host(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)  # Create a game in the lobby
    player = create_player(db, game.id)  # Player is host by default

    # Try to delete the owner from the lobby
    response = test_client.delete(f"/game/{game.id}/leave/{player.id}")
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == f"""Player {player.name} has left the game."""
    )


def test_leave_in_game_host(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.INGAME)  # Create a started game
    player = create_player(db, game.id)  # Player is host by default

    # Remove host
    response = test_client.delete(f"/game/{game.id}/leave/{player.id}")
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == f"Player {player.name} has left the game."
    )


def test_delete_nonexistent_player(test_client):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY)  # Create a started game

    # Try to delete non-existent user
    response = test_client.delete(f"/game/{game.id}/leave/-1")
    assert response.status_code == 404
