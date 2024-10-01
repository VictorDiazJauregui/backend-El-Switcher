import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_db

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test client
client = TestClient(app)

# Create the database tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    yield client

def test_leave_lobby(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Agustin",
        "gameName": "test1", 
        "minPlayers": 2,
        "maxPlayers": 4,
    })
    data = response.json()
    game_id = data["gameId"]
    
    # Add a player to the lobby
    response = test_client.post(f"/game/{game_id}/join", json={ "playerName": "Agustin2"})
    player_data = response.json()
    player_id = player_data["playerId"]
    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "Agustin3"})

    # Delete player from the lobby
    response = test_client.delete(f"/game/{game_id}/leave/{player_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"""Player {player_data["playerName"]} has left the game."""

def test_leave_lobby_host(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Agustin",
        "gameName": "test2", 
        "minPlayers": 2,
        "maxPlayers": 4,
    })
    data = response.json()
    game_id = data["gameId"]
    owner_id = data["ownerId"]

    # Try to delete the owner from the lobby
    response = test_client.delete(f"/game/{game_id}/leave/{owner_id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Host does not have permission to leave the lobby."

def test_leave_in_game_host(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Agustin",
        "gameName": "test3", 
        "minPlayers": 2,
        "maxPlayers": 4,
    })
    data = response.json()
    game_id = data["gameId"]
    owner_id = data["ownerId"]
    owner_name = "Agustin"

    # Add the minimum number of players
    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "Agustin2"})
    player2_name = response.json()["playerName"]

    # Start game
    response = test_client.post(f"/game/{game_id}/start", json={"playerId": owner_id})
    assert response.status_code == 200

    # Remove host
    response = test_client.delete(f"/game/{game_id}/leave/{owner_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Player {owner_name} has left the game."

def test_delete_nonexistent_player(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Agustin",
        "gameName": "test4", 
        "minPlayers": 2,
        "maxPlayers": 4,
    })
    data = response.json()
    game_id = data["gameId"]

    # Add players
    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "Agustin2"})
    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "Agustin3"})
    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "Agustin4"})

    # Try to delete non-existent user
    response = test_client.delete(f"/game/{game_id}/leave/-1")
    assert response.status_code == 404