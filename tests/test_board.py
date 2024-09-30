import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_db, SquarePiece, Board

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

def test_board(test_client):
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
        board = test_db.query(Board).filter_by(game_id=game_id).first()  # Search for the just created game
        assert board is not None, "Couldn't find board asociated."

        board_id = board.game_id

        # Verificar que las fichas se hayan creado correctamente
        pieces = test_db.query(SquarePiece).filter_by(board_id=board_id).all()  # Filter to show only the pieces of this board
        assert len(pieces) == 36  # 36 pieces total
        assert pieces[0].row == 0  # Check that first piece 
        assert pieces[0].column == 0
        assert pieces[35].row == 5  # Check the position of last piece
        assert pieces[35].column == 5
    finally:
        test_db.close()