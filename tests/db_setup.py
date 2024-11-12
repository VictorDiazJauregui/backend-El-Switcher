import bcrypt
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.db import (
    Base,
    get_db,
    Game,
    Board,
    SquarePiece,
    Player,
    CardMove,
    CardFig,
    FigureType,
    Color,
    Turn,
)
from app.schemas.figures import FigureSchema

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


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


def reset_db():
    # Borra todas las tablas
    Base.metadata.drop_all(bind=engine)

    # Crea las tablas de nuevo
    Base.metadata.create_all(bind=engine)


reset_db()


def create_game(db, game_status, password: str = None):

    game = Game(
        name="test_game",
        max_players=4,
        min_players=2,
        status=game_status,
        turn=Turn.P1,
        password=(
            bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            if password
            else None
        ),
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
        SquarePiece(
            color=Color.GREEN, row=0, column=1, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=0, column=2, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=0, column=3, board_id=board.game_id
        ),
        SquarePiece(color=Color.RED, row=0, column=4, board_id=board.game_id),
        SquarePiece(
            color=Color.GREEN, row=0, column=5, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=1, column=0, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=1, column=1, board_id=board.game_id
        ),
        SquarePiece(color=Color.RED, row=1, column=2, board_id=board.game_id),
        SquarePiece(
            color=Color.GREEN, row=1, column=3, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=1, column=4, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=1, column=5, board_id=board.game_id
        ),
        SquarePiece(color=Color.RED, row=2, column=0, board_id=board.game_id),
        SquarePiece(
            color=Color.GREEN, row=2, column=1, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=2, column=2, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=2, column=3, board_id=board.game_id
        ),
        SquarePiece(color=Color.RED, row=2, column=4, board_id=board.game_id),
        SquarePiece(
            color=Color.GREEN, row=2, column=5, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=3, column=0, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=3, column=1, board_id=board.game_id
        ),
        SquarePiece(color=Color.RED, row=3, column=2, board_id=board.game_id),
        SquarePiece(
            color=Color.GREEN, row=3, column=3, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=3, column=4, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=3, column=5, board_id=board.game_id
        ),
        SquarePiece(color=Color.RED, row=4, column=0, board_id=board.game_id),
        SquarePiece(
            color=Color.GREEN, row=4, column=1, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=4, column=2, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=4, column=3, board_id=board.game_id
        ),
        SquarePiece(color=Color.RED, row=4, column=4, board_id=board.game_id),
        SquarePiece(
            color=Color.GREEN, row=4, column=5, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=5, column=0, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=5, column=1, board_id=board.game_id
        ),
        SquarePiece(color=Color.RED, row=5, column=2, board_id=board.game_id),
        SquarePiece(
            color=Color.GREEN, row=5, column=3, board_id=board.game_id
        ),
        SquarePiece(color=Color.BLUE, row=5, column=4, board_id=board.game_id),
        SquarePiece(
            color=Color.YELLOW, row=5, column=5, board_id=board.game_id
        ),
    ]

    for piece in pieces:
        db.add(piece)
    db.commit()


def create_player(db, game_id):
    player = Player(name="test_player", game_id=game_id, turn=Turn.P1)
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


def create_card_fig(db, game_id, player_id):
    card_fig = CardFig(
        game_id=game_id,
        owner_id=player_id,
        in_hand=True,
        figure=FigureType.EASY_7,
    )
    db.add(card_fig)
    db.commit()
    db.refresh(card_fig)
    return card_fig


def create_figure(card_id):
    return FigureSchema(
        colorCards=[
            {"row": 0, "column": 0, "color": Color.RED.name},
            {"row": 0, "column": 1, "color": Color.RED.name},
        ],
        figureCardId=card_id,
    )
