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

def test_create_game_success(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert "gameId" in data
    assert "ownerId" in data

def test_create_game_missing_fields(test_client):
    response = test_client.post("/game_create", json={})
    assert response.status_code == 422

def test_create_game_empty_ownerName(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "",  # Empty field
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "All fields required"

def test_create_game_empty_gameName(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "",  # Empty field
        "maxPlayers": 3,
        "minPlayers": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "All fields required"

def test_create_game_empty_max_players(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": None,  # Empty field
        "minPlayers": 2
    })
    assert response.status_code == 422  # 422 expected because of the missing field and pydantic validation

def test_create_game_empty_min_players(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": None  # Empty field
    })
    assert response.status_code == 422  # 422 expected because of the missing field and pydantic validation

def test_create_game_invalid_max_players(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 1,  # Invalid case
        "minPlayers": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "maxPlayers must be greater than or equal to minPlayers"

def test_create_game_invalid_min_players(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": 1  # Invalid case
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "minPlayers must be at least 2 and at most 4"

def test_create_game_min_players_exceeds_max(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 3,
        "minPlayers": 4  # Invalid case
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "maxPlayers must be greater than or equal to minPlayers"

def test_create_game_max_players_exceeds_limit(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "Bob",
        "gameName": "Test Game",
        "maxPlayers": 5,  # Invalid case
        "minPlayers": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "maxPlayers must be at least 2 and at most 4"