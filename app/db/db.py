import asyncio
import enum
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Enum,
    ForeignKey,
    Text,
    LargeBinary,
    event,
    DateTime,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from contextlib import contextmanager
from datetime import datetime, timezone
import enum

DATABASE_URL = "mysql+pymysql://root:secret@localhost:33061/switcher"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Context manager to get a database session
db_context = contextmanager(get_db)

# Enumeraciones


class GameStatus(enum.Enum):
    LOBBY = "Lobby"
    INGAME = "Ingame"
    FINISHED = "Finished"


class Turn(enum.Enum):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class FigureType(enum.Enum):
    # Easy figures
    EASY_1 = (1, "Figura Fácil 1")
    EASY_2 = (2, "Figura Fácil 2")
    EASY_3 = (3, "Figura Fácil 3")
    EASY_4 = (4, "Figura Fácil 4")
    EASY_5 = (5, "Figura Fácil 5")
    EASY_6 = (6, "Figura Fácil 6")
    EASY_7 = (7, "Figura Fácil 7")

    # Hard figures
    HARD_1 = (1, "Figura Difícil 1")
    HARD_2 = (2, "Figura Difícil 2")
    HARD_3 = (3, "Figura Difícil 3")
    HARD_4 = (4, "Figura Difícil 4")
    HARD_5 = (5, "Figura Difícil 5")
    HARD_6 = (6, "Figura Difícil 6")
    HARD_7 = (7, "Figura Difícil 7")
    HARD_8 = (8, "Figura Difícil 8")
    HARD_9 = (9, "Figura Difícil 9")
    HARD_10 = (10, "Figura Difícil 10")
    HARD_11 = (11, "Figura Difícil 11")
    HARD_12 = (12, "Figura Difícil 12")
    HARD_13 = (13, "Figura Difícil 13")
    HARD_14 = (14, "Figura Difícil 14")
    HARD_15 = (15, "Figura Difícil 15")
    HARD_16 = (16, "Figura Difícil 16")
    HARD_17 = (17, "Figura Difícil 17")
    HARD_18 = (18, "Figura Difícil 18")


class MoveType(enum.Enum):
    MOV_1 = (1, "CRUCE DIAGONAL CON UN ESPACIO")
    MOV_2 = (2, "CRUCE EN LINEA CON UN ESPACIO")
    MOV_3 = (3, "CRUCE EN LINEA CONTIGUO")
    MOV_4 = (4, "CRUCE DIAGONAL CONTIGUO")
    MOV_5 = (5, "CRUCE EN L A LA IZQUIERDA CON DOS ESPACIOS")
    MOV_6 = (6, "CRUCE EN L A LA DERECHA CON DOS ESPACIOS")
    MOV_7 = (7, "CRUCE EN LINEA AL LATERAL")


class Color(enum.Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    YELLOW = "Yellow"


# Modelo Game
class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    password = Column(LargeBinary, nullable=True)
    max_players = Column(Integer, nullable=False)
    min_players = Column(Integer, nullable=False)
    status = Column(Enum(GameStatus), nullable=False)
    turn = Column(Enum(Turn), nullable=True)

    players = relationship(
        "Player",
        back_populates="game",
        order_by="Player.turn",
        cascade="all, delete-orphan",
    )
    board = relationship(
        "Board",
        uselist=False,
        back_populates="game",
        cascade="all, delete-orphan",
    )
    cardmoves = relationship(
        "CardMove", back_populates="game", cascade="all, delete-orphan"
    )
    cardfigs = relationship(
        "CardFig", back_populates="game", cascade="all, delete-orphan"
    )
    chats = relationship(
        "ChatMessage", back_populates="game", cascade="all, delete-orphan"
    )
    logs = relationship(
        "LogMessage", back_populates="game", cascade="all, delete-orphan"
    )


# Modelo Player
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"))
    turn = Column(Enum(Turn), nullable=True)

    game = relationship("Game", back_populates="players")
    card_moves = relationship("CardMove", back_populates="owner")
    card_figs = relationship(
        "CardFig", back_populates="owner", cascade="all, delete-orphan"
    )
    parallel_boards = relationship(
        "ParallelBoard", back_populates="player", cascade="all, delete-orphan"
    )
    chats = relationship(
        "ChatMessage", back_populates="sender", cascade="all, delete-orphan"
    )


# Modelo Board
class Board(Base):
    __tablename__ = "boards"

    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)
    block_color = Column(Enum(Color), nullable=True, default=None)

    game = relationship("Game", back_populates="board")
    square_pieces = relationship(
        "SquarePiece", back_populates="board", cascade="all, delete-orphan"
    )
    parallel_boards = relationship(
        "ParallelBoard", back_populates="board", cascade="all, delete-orphan"
    )


# Modelo ParallelBoard
class ParallelBoard(Base):
    __tablename__ = "parallel_boards"

    id = Column(
        Integer, primary_key=True
    )  # This is the parallelboard unique id
    board_id = Column(
        Integer, ForeignKey("boards.game_id")
    )  # Same id as board and game
    player_id = Column(
        Integer, ForeignKey("players.id")
    )  # Player who made the move
    state_id = Column(Integer, nullable=False)  # This is the state_id, abrazo.
    # state_id = 1-3, 1 = Inicial, 2 = Primer movimiento, 3 = Segundo movimiento
    state_data = Column(Text, nullable=False)  # JSON string
    move_asociated = Column(
        Integer, ForeignKey("card_moves.id"), nullable=True
    )

    board = relationship("Board", back_populates="parallel_boards")
    player = relationship("Player", back_populates="parallel_boards")


# Modelo CardMove
class CardMove(Base):
    __tablename__ = "card_moves"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    owner_id = Column(Integer, ForeignKey("players.id"))
    move = Column(Enum(MoveType), nullable=False)
    played = Column(Boolean, default=False)

    owner = relationship("Player", back_populates="card_moves")
    game = relationship("Game", back_populates="cardmoves")


# Modelo CardFig
class CardFig(Base):
    __tablename__ = "card_figs"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    owner_id = Column(Integer, ForeignKey("players.id"))
    in_hand = Column(Boolean, default=False)
    figure = Column(Enum(FigureType), nullable=False)
    block = Column(Boolean, default=False)
    valid = Column(Boolean, default=True)

    owner = relationship("Player", back_populates="card_figs")
    game = relationship("Game", back_populates="cardfigs")


# Modelo SquarePiece
class SquarePiece(Base):
    __tablename__ = "square_pieces"

    id = Column(Integer, primary_key=True)
    color = Column(Enum(Color), nullable=False)
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)
    board_id = Column(Integer, ForeignKey("boards.game_id"))
    partial_id = Column(Integer, nullable=True)

    board = relationship("Board", back_populates="square_pieces")


class ChatMessage(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    message = Column(String(100), nullable=False)
    sender_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))

    sender = relationship("Player", back_populates="chats")
    game = relationship("Game", back_populates="chats")


class LogMessage(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    message = Column(String(100), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"))

    game = relationship("Game", back_populates="logs")


# Event listener to set owner_id to None instead of deleting CardMove
@event.listens_for(Player, "before_delete")
def receive_before_delete(mapper, connection, target):
    # Set owner_id to None if it is not already None
    connection.execute(
        CardMove.__table__.update()
        .where(CardMove.owner_id == target.id)
        .values(owner_id=None)
    )
    # Delete CardMove if owner_id is already None
    connection.execute(
        CardMove.__table__.delete()
        .where(CardMove.owner_id == target.id)
        .where(CardMove.owner_id.is_(None))
    )
