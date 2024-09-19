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

def test_add_player_to_game(test_client):
    # First, create a game
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    # Now, add a player to the game
    response = test_client.post(f"/game/{game_id}/join", json={"name": "test_player"})
    assert response.status_code == 200
    data = response.json()
    assert "playerId" in data
    assert data["name"] == "test_player"

def test_add_player_to_game_missing_fields(test_client):
    response = test_client.post("/game/1/join", json={})
    assert response.status_code == 422

def test_join_full_game(test_client):
    # First, create a game
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 2,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    response = test_client.post(f"/game/{game_id}/join", json={"name": "test_player2"})
    assert response.status_code == 200

    response = test_client.post(f"/game/{game_id}/join", json={"name": "test_player3"})
    assert response.status_code == 400
    assert response.json()["detail"] == f"Game {game_id} is full."

def test_join_started_game(test_client):
    # First, create a game
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    # Add min players to the game
    response = test_client.post(f"/game/{game_id}/join", json={"name": "test_player"})
    assert response.status_code == 200

    response = test_client.post(f"/game/{game_id}/join", json={"name": "test_player2"})
    assert response.status_code == 200

    # Now, start the game
    response = test_client.post(f"/game/{game_id}/start")
    assert response.status_code == 200
    
    # Now, add a player to the game
    response = test_client.post(f"/game/{game_id}/join", json={"name": "test_player"})
    assert response.status_code == 400
    assert response.json()["detail"] == f"Game {game_id} is already in progress."

def test_add_player_to_nonexistent_game(test_client):
    """ Test adding a player to a non-existent game """
    nonexistent_game_id = 999  # Assuming this game ID does not exist
    response = test_client.post(f"/game/{nonexistent_game_id}/join", json={"name": "Alice"})
    
    # The expected response should be 404 Not Found
    assert response.status_code == 404
    assert response.json()["detail"] == f"Game with id {nonexistent_game_id} does not exist."