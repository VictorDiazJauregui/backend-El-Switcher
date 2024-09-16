import pytest
from fastapi.testclient import TestClient
from app.main import app  # Asegúrate de que 'app' es tu instancia FastAPI

client = TestClient(app)

def test_create_game_success():
    response = client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert "gameId" in data
    assert "ownerId" in data
    assert data["ownerId"] == 0  # Ensure that ownerId is 0

def test_create_game_missing_fields():
    response = client.post("/game_create", json={})
    assert response.status_code == 422

def test_create_game_empty_ownerName():
    response = client.post("/game_create", json={
        "ownerName": "",  # Empty field
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "All fields required"

def test_create_game_empty_gameName():
    response = client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "",  # Empty field
        "maxPlayers": 3,
        "minPlayers": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "All fields required"

def test_create_game_empty_max_players():
    response = client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": None,  # Empty field
        "minPlayers": 2
    })
    assert response.status_code == 422 # 422 expected because of the missing field and pydantic validation

def test_create_game_empty_min_players():
    response = client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": None  # Empty field
    })
    assert response.status_code == 422 # 422 expected because of the missing field and pydantic validation

def test_create_game_invalid_max_players():
    response = client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 1,  # Invalid case
        "minPlayers": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "maxPlayers must be greater than or equal to minPlayers"

def test_create_game_invalid_min_players():
    response = client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": 1  # Invalid case
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "minPlayers must be at least 2 and at most 4"

def test_create_game_min_players_exceeds_max():
    response = client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": 4  # Invalid case
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "maxPlayers must be greater than or equal to minPlayers"

def test_create_game_max_players_exceeds_limit():
    response = client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 5,  # Invalid case
        "minPlayers": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "maxPlayers must be at least 2 and at most 4"
