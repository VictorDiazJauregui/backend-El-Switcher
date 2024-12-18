from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class ParallelBoard(Base):
    __tablename__ = "parallel_boards"

    id = Column(Integer, primary_key=True)  # This is the parallelboard unique id
    board_id = Column(Integer, ForeignKey("boards.game_id"))  # Same id as board and game
    player_id = Column(Integer, ForeignKey("players.id"))  # Player who made the move
    state_id = Column(Integer, nullable=False)  # This is the state_id, abrazo.
    # state_id = 1-3, 1 = Inicial, 2 = Primer movimiento, 3 = Segundo movimiento
    state_data = Column(Text, nullable=False)  # JSON string
    move_asociated = Column(Integer, ForeignKey("card_moves.id"), nullable=True)

    board = relationship("Board", back_populates="parallel_boards")
    player = relationship("Player", back_populates="parallel_boards")