from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.enums import Color


class SquarePiece(Base):
    __tablename__ = "square_pieces"

    id = Column(Integer, primary_key=True)
    color = Column(Enum(Color), nullable=False)
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)
    board_id = Column(Integer, ForeignKey("boards.game_id"))
    partial_id = Column(Integer, nullable=True)

    board = relationship("Board", back_populates="square_pieces")
