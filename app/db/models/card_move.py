from sqlalchemy import Column, Integer, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.enums import MoveType

class CardMove(Base):
    __tablename__ = "card_moves"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    owner_id = Column(Integer, ForeignKey("players.id"))
    move = Column(Enum(MoveType), nullable=False)
    played = Column(Boolean, default=False)

    owner = relationship("Player", back_populates="card_moves")
    game = relationship("Game", back_populates="cardmoves")