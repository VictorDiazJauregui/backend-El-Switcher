import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_game_success():
    response = client.post("/new", json={
        "ownerName": "Alice",
        "gameName": "Test Game",
        "maxPlayers": 4
    })
    assert response.status_code == 200
    data = response.json()
    assert "gameId" in data
    assert "gameName" in data
    assert "maxPlayers" in data
    assert "players" in data
    assert data["players"] == ["Alice"]

def test_create_game_invalid_data():
    response = client.post("/new", json={
        "ownerName": "",
        "gameName": "Test Game",
        "maxPlayers": 4
    })
    assert response.status_code == 422  # Unprocessable Entity (Validation Error)
    assert response.json()["detail"] == "All fields required"

def test_create_game_max_players_less():
    response = client.post("/new", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 1  # Invalid case: maxPlayers must be at least 2
    })
    assert response.status_code == 400  # Bad Request
    assert response.json()["detail"] == "maxPlayers must be at least 2"

def test_create_game_max_players_more():
    response = client.post("/new", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 5  # Edge case: maxPlayers must be at most 4
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "maxPlayers must be at most 4"

def test_create_game_missing_fields():
    response = client.post("/new", json={
        "ownerName": "Charlie"
        # Missing gameName and maxPlayers
    })
    assert response.status_code == 422  # Unprocessable Entity (Validation Error)
