from sqlalchemy import Column, Integer, String, LargeBinary, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.enums import GameStatus, Turn


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
