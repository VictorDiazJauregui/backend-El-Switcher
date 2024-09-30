import pytest
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.db.db import Base, get_db, Player, CardMove, CardFig, FigureType, MoveType
from app.main import app
from app.services.cards import deal_movement_cards, deal_figure_cards, add_cards_to_db

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

# Setup test client
client = TestClient(app)

# Borra todas las tablas y crea de nuevo
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_add_cards_to_db(test_db):
    game_id = 1
    add_cards_to_db(game_id, test_db)

    moves = test_db.query(CardMove).filter_by(game_id=game_id).all()
    figs = test_db.query(CardFig).filter_by(game_id=game_id).all()

    assert len(moves) == len(MoveType) * 7  # 7 cards for each type of movement
    assert len(figs) == len(FigureType) * 2  # 2 cards for each type of figure

def test_deal_movement_cards(test_db):
    game_id = 1
    player = Player(id=1, game_id=game_id, name="Player 1")
    test_db.add(player)
    test_db.commit()

    result = deal_movement_cards(game_id, player.id, test_db)
    
    assert len(result) == 3  # Only 3 cards per player

def test_deal_figure_cards(test_db):
    game_id = 1
    player = Player(id=2, game_id=game_id, name="Player 2")
    test_db.add(player)
    test_db.commit()

    response = deal_figure_cards(game_id, test_db)

    assert len(response) == 2  # Make sure that the response is fro 2 players
    player_cards = response[0]['cards']
    assert len(player_cards) == 3  # Only 3 cards per player
