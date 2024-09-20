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
    edit = "temp"

class MoveType(enum.Enum):
    edit = "temp"

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
    type_move = Column(Enum(MoveType), nullable=False)

    owner = relationship("Player", back_populates="card_moves")

#    def take():

# Modelo CardFig
class CardFig(Base):
    __tablename__ = 'card_figs'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('players.id'))
    figure = Column(Enum(FigureType), nullable=False)
    block = Column(Boolean, default=False)
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
