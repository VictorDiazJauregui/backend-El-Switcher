from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.enums import Color

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