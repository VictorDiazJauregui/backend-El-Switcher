import pytest
from app.db.db import GameStatus, Player
from .db_setup import (
    client,
    TestingSessionLocal,
    create_game,
    create_player,
)


@pytest.fixture(scope="module")
def test_client():
    yield client


def test_add_player_to_game(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)

    # Now, add a player to the game
    response = test_client.post(
        f"/game/{game.id}/join", json={"playerName": "test_player"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "playerId" in data
    assert data["playerName"] == "test_player"


def test_add_player_to_game_with_correct_password(test_client):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY, password="securepassword")

    # Now, try to add a player with the correct password
    response = test_client.post(
        f"/game/{game.id}/join",
        json={
            "playerName": "Bob",
            "password": "securepassword",
        },
    )

    assert response.status_code == 200
    player_data = response.json()
    assert "playerId" in player_data
    assert "playerName" in player_data


def test_add_players_to_game_with_correct_password(test_client):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY, password="securepassword")

    # Add 4 players to the game
    player_names = ["Bob", "Alice", "Charlie", "David"]
    for player_name in player_names:
        response = test_client.post(
            f"/game/{game.id}/join",
            json={
                "playerName": player_name,
                "password": "securepassword",
            },
        )
        assert response.status_code == 200
        player_data = response.json()
        assert "playerId" in player_data
        assert player_data["playerName"] == player_name

    # Verify all players are in the game
    connected_players = (
        db.query(Player).filter(Player.game_id == game.id).all()
    )
    assert len(connected_players) == 4
    connected_player_names = [
        player.name for player in connected_players
    ]  # Get list of player names
    for name in player_names:
        assert name in connected_player_names  # Compare strings with strings


def test_add_player_to_game_with_incorrect_password(test_client):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY, password="password")

    # Now, try to add a player with an incorrect password
    response = test_client.post(
        f"/game/{game.id}/join",
        json={
            "playerName": "Bob",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect password."


def test_join_public_game_with_password(test_client):
    db = TestingSessionLocal()
    # Create game without password
    game = create_game(db, GameStatus.LOBBY)

    # Try to join with a password
    response = test_client.post(
        f"/game/{game.id}/join",
        json={"playerName": "test_player", "password": "somepassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Game does not have a password."


def test_join_private_game_without_password(test_client):
    db = TestingSessionLocal()
    # Create game with password
    game = create_game(db, GameStatus.LOBBY, password="securepassword")

    # Try to join without providing password
    response = test_client.post(
        f"/game/{game.id}/join",
        json={"playerName": "test_player"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Password required to join game."


def test_add_player_to_game_missing_fields(test_client):
    response = test_client.post("/game/1/join", json={})
    assert response.status_code == 422


def test_join_full_game(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)
    create_player(db, game.id)
    create_player(db, game.id)
    create_player(db, game.id)
    create_player(db, game.id)

    response = test_client.post(
        f"/game/{game.id}/join", json={"playerName": "test_player3"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == f"Game {game.id} is full."


def test_join_started_game(test_client):
    db = TestingSessionLocal()
    # First, create a started game
    game = create_game(db, GameStatus.INGAME)

    # Now, add a player to the game
    response = test_client.post(
        f"/game/{game.id}/join", json={"playerName": "test_player"}
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == f"Game {game.id} is already in progress."
    )


def test_add_player_to_nonexistent_game(test_client):
    """Test adding a player to a non-existent game"""
    nonexistent_game_id = 999  # Assuming this game ID does not exist
    response = test_client.post(
        f"/game/{nonexistent_game_id}/join", json={"playerName": "Alice"}
    )

    # The expected response should be 404 Not Found
    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == f"Game with id {nonexistent_game_id} does not exist."
    )
