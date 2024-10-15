import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_db, Board, Color, SquarePiece, CardMove, Player, Game , Turn, GameStatus, MoveType

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

def create_game(db):
    game = Game(
        name = "test_game",
        max_players = 4,
        min_players = 2,
        status = GameStatus.INGAME,
        turn = Turn.P1
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

def add_example_board(db, game_id):
    board = Board(game_id=game_id, block_color=Color.RED)
    db.add(board)
    db.commit()
    db.refresh(board)

    pieces = [
        SquarePiece(color=Color.RED, row=0, column=0, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=0, column=1, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=0, column=2, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=0, column=3, board_id=board.game_id),
        SquarePiece(color=Color.RED, row=0, column=4, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=0, column=5, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=1, column=0, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=1, column=1, board_id=board.game_id),
        SquarePiece(color=Color.RED, row=1, column=2, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=1, column=3, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=1, column=4, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=1, column=5, board_id=board.game_id),
        SquarePiece(color=Color.RED, row=2, column=0, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=2, column=1, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=2, column=2, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=2, column=3, board_id=board.game_id),
        SquarePiece(color=Color.RED, row=2, column=4, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=2, column=5, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=3, column=0, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=3, column=1, board_id=board.game_id),
        SquarePiece(color=Color.RED, row=3, column=2, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=3, column=3, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=3, column=4, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=3, column=5, board_id=board.game_id),
        SquarePiece(color=Color.RED, row=4, column=0, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=4, column=1, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=4, column=2, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=4, column=3, board_id=board.game_id),
        SquarePiece(color=Color.RED, row=4, column=4, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=4, column=5, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=5, column=0, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=5, column=1, board_id=board.game_id),
        SquarePiece(color=Color.RED, row=5, column=2, board_id=board.game_id),
        SquarePiece(color=Color.GREEN, row=5, column=3, board_id=board.game_id),
        SquarePiece(color=Color.BLUE, row=5, column=4, board_id=board.game_id),
        SquarePiece(color=Color.YELLOW, row=5, column=5, board_id=board.game_id),
    ]

    for piece in pieces:
        db.add(piece)
    db.commit()

def create_player(db, game_id):
    player = Player(name="test_player", game_id=game_id, turn = Turn.P1)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

def create_card_move(db, player_id, move_type):
    card_move = CardMove(owner_id=player_id, move=move_type)
    db.add(card_move)
    db.commit()
    db.refresh(card_move)
    return card_move

def test_make_move(test_client):
    db = TestingSessionLocal()
    try:
        game = create_game(db)
        add_example_board(db, game.id)
        player = create_player(db, game.id)
        card_move = create_card_move(db, player.id, MoveType.MOV_3)
        piece1 = db.query(SquarePiece).filter(SquarePiece.board_id == game.id).first()
        piece2 = db.query(SquarePiece).filter(SquarePiece.board_id == game.id, SquarePiece.id != piece1.id).first()

        movementCardId = card_move.id
        squarePieceId1 = piece1.id
        squarePieceId2 = piece2.id
        
        response = test_client.post(f"/game/{game.id}/move/{player.id}", json={
            "movementCardId": movementCardId,
            "squarePieceId1": squarePieceId1,
            "squarePieceId2": squarePieceId2
        })
        assert response.status_code == 200
    finally:
        db.close()

def generate_square_piece(row, column):
    return SquarePiece(row=row, column=column)

# Generate test cases for each MoveType
test_cases = {
    MoveType.MOV_1: { #CRUCE DIAGONAL CON UN ESPACIO
        "pass": (generate_square_piece(0, 0), generate_square_piece(2, 2)),
        "fail": (generate_square_piece(0, 0), generate_square_piece(1, 1))
    },
    MoveType.MOV_2: { #CRUCE EN LINEA CON UN ESPACIO
        "pass": (generate_square_piece(0, 0), generate_square_piece(2, 0)),
        "fail": (generate_square_piece(0, 0), generate_square_piece(1, 1))
    },
    MoveType.MOV_3: { #CRUCE EN LINEA CONTIGUO
        "pass": (generate_square_piece(0, 0), generate_square_piece(1, 0)),
        "fail": (generate_square_piece(0, 0), generate_square_piece(2, 2))
    },
    MoveType.MOV_4: { #CRUCE DIAGONAL CONTIGUO
        "pass": (generate_square_piece(0, 0), generate_square_piece(1, 1)),
        "fail": (generate_square_piece(0, 0), generate_square_piece(2, 2))
    },
    MoveType.MOV_5: { #CRUCE EN L A LA IZQUIERDA CON DOS ESPACIOS
        "pass": (generate_square_piece(2, 1), generate_square_piece(0, 0)),
        "fail": (generate_square_piece(0, 0), generate_square_piece(1, 1))
    },
    MoveType.MOV_6: { #CRUCE EN L A LA DERECHA CON DOS ESPACIOS
        "pass": (generate_square_piece(0, 0), generate_square_piece(2, 1)),
        "fail": (generate_square_piece(0, 0), generate_square_piece(1, 1))
    },
    MoveType.MOV_7: { #CRUCE EN LINEA AL LATERAL
        "pass": (generate_square_piece(0, 2), generate_square_piece(0, 5)),
        "fail": (generate_square_piece(0, 0), generate_square_piece(1, 1))
    }
}


@pytest.mark.parametrize("move_type, pieces, expected", [
    (MoveType.MOV_1, test_cases[MoveType.MOV_1]["pass"], True),
    (MoveType.MOV_2, test_cases[MoveType.MOV_2]["pass"], True),
    (MoveType.MOV_3, test_cases[MoveType.MOV_3]["pass"], True),
    (MoveType.MOV_4, test_cases[MoveType.MOV_4]["pass"], True),
    (MoveType.MOV_5, test_cases[MoveType.MOV_5]["pass"], True),
    (MoveType.MOV_6, test_cases[MoveType.MOV_6]["pass"], True),
    (MoveType.MOV_7, test_cases[MoveType.MOV_7]["pass"], True)
])
def test_move_types(test_client, move_type, pieces, expected):
    db = TestingSessionLocal()
    try:
        game = create_game(db)
        add_example_board(db, game.id)
        player = create_player(db, game.id)
        card_move = create_card_move(db, player.id, move_type)
        
        piece1_coords, piece2_coords = pieces
        piece1 = db.query(SquarePiece).filter(SquarePiece.board_id == game.id, SquarePiece.row == piece1_coords.row, SquarePiece.column == piece1_coords.column).first()
        piece2 = db.query(SquarePiece).filter(SquarePiece.board_id == game.id, SquarePiece.row == piece2_coords.row, SquarePiece.column == piece2_coords.column).first()

        movementCardId = card_move.id
        squarePieceId1 = piece1.id
        squarePieceId2 = piece2.id
        
        response = test_client.post(f"/game/{game.id}/move/{player.id}", json={
            "movementCardId": movementCardId,
            "squarePieceId1": squarePieceId1,
            "squarePieceId2": squarePieceId2
        })
        assert response.status_code == 200
    finally:
        db.close()

@pytest.mark.parametrize("move_type, pieces, expected", [
    (MoveType.MOV_1, test_cases[MoveType.MOV_1]["fail"], False),
    (MoveType.MOV_2, test_cases[MoveType.MOV_2]["fail"], False),
    (MoveType.MOV_3, test_cases[MoveType.MOV_3]["fail"], False),
    (MoveType.MOV_4, test_cases[MoveType.MOV_4]["fail"], False),
    (MoveType.MOV_5, test_cases[MoveType.MOV_5]["fail"], False),
    (MoveType.MOV_6, test_cases[MoveType.MOV_6]["fail"], False),
    (MoveType.MOV_7, test_cases[MoveType.MOV_7]["fail"], False),
])
def test_move_types_fail(test_client, move_type, pieces, expected):
    db = TestingSessionLocal()
    try:
        game = create_game(db)
        add_example_board(db, game.id)
        player = create_player(db, game.id)
        card_move = create_card_move(db, player.id, move_type)
        
        piece1_coords, piece2_coords = pieces
        piece1 = db.query(SquarePiece).filter(SquarePiece.board_id == game.id, SquarePiece.row == piece1_coords.row, SquarePiece.column == piece1_coords.column).first()
        piece2 = db.query(SquarePiece).filter(SquarePiece.board_id == game.id, SquarePiece.row == piece2_coords.row, SquarePiece.column == piece2_coords.column).first()

        movementCardId = card_move.id
        squarePieceId1 = piece1.id
        squarePieceId2 = piece2.id
        
        try:
            response = test_client.post(f"/game/{game.id}/move/{player.id}", json={
                "movementCardId": movementCardId,
                "squarePieceId1": squarePieceId1,
                "squarePieceId2": squarePieceId2
            })
            assert expected == True
        except Exception as e:
            assert expected == False
                
    finally:
        db.close()