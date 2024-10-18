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

def test_add_player_to_game(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.LOBBY)
    
    # Now, add a player to the game
    response = test_client.post(f"/game/{game.id}/join", json={"playerName": "test_player"})
    assert response.status_code == 200
    data = response.json()
    assert "playerId" in data
    assert data["playerName"] == "test_player"

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

    response = test_client.post(f"/game/{game.id}/join", json={"playerName": "test_player3"})
    assert response.status_code == 400
    assert response.json()["detail"] == f"Game {game.id} is full."

def test_join_started_game(test_client):
    db = TestingSessionLocal()
    # First, create a started game
    game = create_game(db, GameStatus.INGAME)

    # Now, add a player to the game
    response = test_client.post(f"/game/{game.id}/join", json={"playerName": "test_player"})
    assert response.status_code == 400
    assert response.json()["detail"] == f"Game {game.id} is already in progress."

def test_add_player_to_nonexistent_game(test_client):
    """ Test adding a player to a non-existent game """
    nonexistent_game_id = 999  # Assuming this game ID does not exist
    response = test_client.post(f"/game/{nonexistent_game_id}/join", json={"playerName": "Alice"})
    
    # The expected response should be 404 Not Found
    assert response.status_code == 404
    assert response.json()["detail"] == f"Game with id {nonexistent_game_id} does not exist."