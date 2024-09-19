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

def test_get_game_list(test_client):
    
    test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
   
    response = test_client.get("/game_list")
    assert response.status_code == 200
    data = response.json()

def test_get_list_more_games(test_client):
    
    test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    
    test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game2",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    
    response = test_client.get("/game_list")
    assert response.status_code == 200
