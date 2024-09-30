import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_db
import logging

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
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

# Create the test client
client = TestClient(app)

# Create the database tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    yield client



def test_end_turn_success(test_client):

     # First, create a game
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 2,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]

    # Add min players to the game
    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "test_player"})

    assert response.status_code == 200, "Could not add player to game."

    test_player_data = response.json()
    test_player_id = test_player_data["playerId"]
    test_player_name = test_player_data["playerName"]

    #Start the game
    response = test_client.post(f"/game/{game_id}/start")
    assert response.status_code == 200

    response = client.post(f"/game/{game_id}/end_turn/{test_player_id}")
    assert response.status_code == 200

    assert response.json() ==  {'message': "Player test_player has ended their turn."}


def test_end_turn_invalid_game_id(test_client):
    response = client.post("/game/999/end_turn/1")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Game with id 999 does not exist."}

def test_end_turn_invalid_player_id(test_client):
    response = client.post("/game/1/end_turn/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Player with id 999 does not exist."}

def test_end_turn_not_player_turn(test_client):

    # First, create a game
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 2,
        "minPlayers": 2
    })
    game_data = response.json()
    game_id = game_data["gameId"]
    owner_id = game_data["ownerId"]

    # Add min players to the game
    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "test_player"})
    assert response.status_code == 200
    test_player_data = response.json()
    test_player_id = test_player_data["playerId"]

    #Start the game
    response = test_client.post(f"/game/{game_id}/start")
    assert response.status_code == 200

    response = client.post(f"/game/{game_id}/end_turn/{owner_id}")
    assert response.status_code == 400
    assert response.json() == {"detail": f"It's not {owner_id} turn."}

def test_end_turn_game_not_started(test_client):
        # First, create a game
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 2,
        "minPlayers": 2
        })
    game_data = response.json()
    game_id = game_data["gameId"]

    # Add min players to the game
    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "test_player"})
    assert response.status_code == 200
    test_player_data = response.json()
    test_player_id = test_player_data["playerId"]

    response = client.post(f"/game/{game_id}/end_turn/{test_player_id}")
    assert response.status_code == 400
    assert response.json() == {"detail": f"Game {game_id} is not in progress."}
