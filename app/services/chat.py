from app.schemas.chat import ChatMessageSchema
from app.db.db import ChatMessage
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
import app.models.broadcast


async def get_chat_history(game_id: int, db: Session):
    result = db.execute(
        select(ChatMessage)
        .options(selectinload(ChatMessage.sender))
        .where(ChatMessage.game_id == game_id)
        .order_by(ChatMessage.created_at)
    )
    return result.scalars().all()
