import pytest
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.db.db import Base, get_db, CardMove, CardFig, FigureType, MoveType
from app.main import app
from app.services.cards import deal_movement_cards

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

# Borra todas las tablas
Base.metadata.drop_all(bind=engine)

# Crea las tablas de nuevo
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_client():
    yield client


@pytest.mark.skip(reason="Deprecated test")
def test_add_cards_to_db(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    assert response.status_code == 200
    game_id = response.json().get("gameId")

    test_db = TestingSessionLocal()

    try:
        moves = test_db.query(CardMove).filter_by(game_id=game_id).all()
        figs = test_db.query(CardFig).filter_by(game_id=game_id).all()

        assert len(moves) == len(MoveType) * 7  # 7 cards for each type of movement
        assert len(figs) == len(FigureType) * 2  # 2 cards for each type of figure
    finally:
        test_db.close()


@pytest.mark.skip(reason="Deprecated test")
def test_deal_movement_cards(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    assert response.status_code == 200
    game_id = response.json()["gameId"]
    owner_id = response.json()["ownerId"]

    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "Player 2"})
    player2_id = response.json()["playerId"]

    test_db = TestingSessionLocal()
    try:
        result1 = deal_movement_cards(game_id, owner_id, test_db)
        result2 = deal_movement_cards(game_id, player2_id, test_db)

        assert len(result1) == 3  # Only 3 cards per player
        assert len(result2) == 3  # Only 3 cards per player

        # Again!
        result1 = deal_movement_cards(game_id, owner_id, test_db)
        result2 = deal_movement_cards(game_id, player2_id, test_db)

        assert len(result1) == 3  # Only 3 cards per player
        assert len(result2) == 3  # Only 3 cards per player
    finally:
        test_db.close()
"""
@pytest.mark.skip(reason="Deprecated test")
def test_deal_figure_cards(test_client):
    response = test_client.post("/game_create", json={
        "ownerName": "test_owner",
        "gameName": "test_game",
        "maxPlayers": 4,
        "minPlayers": 2
    })
    assert response.status_code == 200
    game_id = response.json()["gameId"]

    response = test_client.post(f"/game/{game_id}/join", json={"playerName": "Player 2"})

    test_db = TestingSessionLocal()

    try:
        response = deal_figure_cards(game_id, test_db)

        assert len(response) == 2  # Make sure that the response is for 2 players
        player_cards = response[0]['cards']
        assert len(player_cards) == 3  # Only 3 cards per player
    finally:
        test_db.close()

"""
