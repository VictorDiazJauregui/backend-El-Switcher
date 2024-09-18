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

def test_game_list():
    response = client.get("/game_list")
    assert response.status_code == 200
    response = response.json()
    assert "games" in response
    assert isinstance(response["games"], list)  # Verify that "games" is a list