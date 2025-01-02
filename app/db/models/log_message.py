from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base


class LogMessage(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    message = Column(String(100), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"))

    game = relationship("Game", back_populates="logs")
