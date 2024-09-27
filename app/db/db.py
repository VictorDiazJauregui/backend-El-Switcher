from sqlalchemy import create_engine, Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
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

# Enumeraciones

class GameStatus(enum.Enum):
    LOBBY = 'Lobby'
    INGAME = 'Ingame'
    FINISHED = 'Finished'

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
    HARD_1 = (8, "Figura Difícil 1")
    HARD_2 = (9, "Figura Difícil 2")
    HARD_3 = (10, "Figura Difícil 3")
    HARD_4 = (11, "Figura Difícil 4")
    HARD_5 = (12, "Figura Difícil 5")
    HARD_6 = (13, "Figura Difícil 6")
    HARD_7 = (14, "Figura Difícil 7")
    HARD_8 = (15, "Figura Difícil 8")
    HARD_9 = (16, "Figura Difícil 9")
    HARD_10 = (17, "Figura Difícil 10")
    HARD_11 = (18, "Figura Difícil 11")
    HARD_12 = (19, "Figura Difícil 12")
    HARD_13 = (20, "Figura Difícil 13")
    HARD_14 = (21, "Figura Difícil 14")
    HARD_15 = (22, "Figura Difícil 15")
    HARD_16 = (23, "Figura Difícil 16")
    HARD_17 = (24, "Figura Difícil 17")
    HARD_18 = (25, "Figura Difícil 18")


class MoveType(enum.Enum):
    MOV_1 = (1, "Movimiento 1")
    MOV_2 = (2, "Movimiento 2")
    MOV_3 = (3, "Movimiento 3")
    MOV_4 = (4, "Movimiento 4")
    MOV_5 = (5, "Movimiento 5")
    MOV_6 = (6, "Movimiento 6")
    MOV_7 = (7, "Movimiento 7")
    MOV_8 = (8, "Movimiento 8")
    MOV_9 = (9, "Movimiento 9")
    MOV_10 = (10, "Movimiento 10")
    MOV_11 = (11, "Movimiento 11")
    MOV_12 = (12, "Movimiento 12")
    MOV_13 = (13, "Movimiento 13")
    MOV_14 = (14, "Movimiento 14")
    MOV_15 = (15, "Movimiento 15")
    MOV_16 = (16, "Movimiento 16")
    MOV_17 = (17, "Movimiento 17")
    MOV_18 = (18, "Movimiento 18")
    MOV_19 = (19, "Movimiento 19")
    MOV_20 = (20, "Movimiento 20")
    MOV_21 = (21, "Movimiento 21")
    MOV_22 = (22, "Movimiento 22")
    MOV_23 = (23, "Movimiento 23")
    MOV_24 = (24, "Movimiento 24")
    MOV_25 = (25, "Movimiento 25")
    MOV_26 = (26, "Movimiento 26")
    MOV_27 = (27, "Movimiento 27")
    MOV_28 = (28, "Movimiento 28")
    MOV_29 = (29, "Movimiento 29")
    MOV_30 = (30, "Movimiento 30")
    MOV_31 = (31, "Movimiento 31")
    MOV_32 = (32, "Movimiento 32")
    MOV_33 = (33, "Movimiento 33")
    MOV_34 = (34, "Movimiento 34")
    MOV_35 = (35, "Movimiento 35")
    MOV_36 = (36, "Movimiento 36")
    MOV_37 = (37, "Movimiento 37")
    MOV_38 = (38, "Movimiento 38")
    MOV_39 = (39, "Movimiento 39")
    MOV_40 = (40, "Movimiento 40")

class Color(enum.Enum):
    RED = 'Red'
    GREEN = 'Green'
    BLUE = 'Blue'
    YELLOW = 'Yellow'

# Modelo Game
class Game(Base):
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    password = Column(String(25), nullable=True)
    max_players = Column(Integer, nullable=False)
    min_players = Column(Integer, nullable=False)
    status = Column(Enum(GameStatus), nullable=False)
    turn = Column(Enum(Turn), nullable=True)

    players = relationship("Player", back_populates="game")
    board = relationship("Board", uselist=False, back_populates="game")

#    def end_game():
#    def next_turn():

    

# Modelo Player
class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'))
    turn = Column(Enum(Turn), nullable=True)
    
    game = relationship("Game", back_populates="players")
    card_moves = relationship("CardMove", back_populates="owner")
    card_figs = relationship("CardFig", back_populates="owner")

#    def join():
#    def leave():

# Modelo Board
class Board(Base):
    __tablename__ = 'boards'
    
    id = Column(Integer, primary_key=True)
    block_color = Column(Enum(Color))
    game_id = Column(Integer, ForeignKey('games.id'))
    
    game = relationship("Game", back_populates="board")
    square_pieces = relationship("SquarePiece", back_populates="board")

#    def update_color():
#    def mover_fichas():

# Modelo CardMove
class CardMove(Base):
    __tablename__ = 'card_moves'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('players.id'))
    move = Column(Enum(MoveType), nullable=False)

    owner = relationship("Player", back_populates="card_moves")

#    def take():

# Modelo CardFig
class CardFig(Base):
    __tablename__ = 'card_figs'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('players.id'))
    figure = Column(Enum(FigureType), nullable=False)
    blocked = Column(Boolean, default=False)
    valid = Column(Boolean, default=True)

    owner = relationship("Player", back_populates="card_figs")

#    def take():
#    def block():
#    def unblock():
#    def check():

# Modelo SquarePiece
class SquarePiece(Base):
    __tablename__ = 'square_pieces'
    
    id = Column(Integer, primary_key=True)
    color = Column(Enum(Color), nullable=False)
    position = Column(String(2), nullable=False)
    board_id = Column(Integer, ForeignKey('boards.id'))

    board = relationship("Board", back_populates="square_pieces")

#    def change_pos():
