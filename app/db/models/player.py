from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.enums import Turn

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