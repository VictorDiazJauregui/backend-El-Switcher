import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_db
from app.db.db import GameStatus

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

################# Test cases for /game/{game_id}/start #################

def test_start_game(test_client):
    # First, create a game
    response = test_client.post("/game_create/", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    # Add enough players to start the game
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player1"})
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player2"})

    # Now, start the game
    response = test_client.post(f"/game/{game_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game_id
    assert data["status"] == GameStatus.INGAME.value

def test_start_full_game(test_client):
    # First, create a game
    response = test_client.post("/game_create/", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 2,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    # Add enough players to start the game
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player1"})
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player2"})

    # Now, start the game
    response = test_client.post(f"/game/{game_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game_id
    assert data["status"] == GameStatus.INGAME.value

def test_start_full_game_4_players(test_client):
    # First, create a game
    response = test_client.post("/game_create/", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    # Add enough players to start the game
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player1"})
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player2"})
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player3"})
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player4"})

    # Now, start the game
    response = test_client.post(f"/game/{game_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game_id
    assert data["status"] == GameStatus.INGAME.value

def test_start_already_started_game(test_client):
    # First, create a game
    response = test_client.post("/game_create/", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    # Add enough players to start the game
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player1"})
    test_client.post(f"/game/{game_id}/join", json={"name": "test_player2"})

    # Start the game
    test_client.post(f"/game/{game_id}/start")

    # Try to start the game again
    response = test_client.post(f"/game/{game_id}/start")
    assert response.status_code == 400
    assert response.json()["detail"] == f"Game {game_id} is already in progress."

def test_not_enough_players(test_client):
    response = test_client.post("/game_create/", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    response = test_client.post(f"/game/{game_id}/start")
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough players to start the game."

def test_start_nonexistent_game(test_client):
    """ Test starting a non-existent game """
    nonexistent_game_id = 999  # Assuming this game ID does not exist
    response = test_client.post(f"/game/{nonexistent_game_id}/start")
    
    # The expected response should be 404 Not Found
    assert response.status_code == 404
    assert response.json()["detail"] == f"Game with id {nonexistent_game_id} does not exist."
