from sqlalchemy import Column, Integer, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.enums import FigureType


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
