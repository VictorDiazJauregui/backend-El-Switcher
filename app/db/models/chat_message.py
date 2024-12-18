from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class ChatMessage(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    message = Column(String(100), nullable=False)
    sender_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))

    sender = relationship("Player", back_populates="chats")
    game = relationship("Game", back_populates="chats")