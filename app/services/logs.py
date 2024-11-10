from app.schemas.logs import LogMessageSchema, SingleLogMessageSchema
from app.db.db import LogMessage
from app.models.broadcast import Broadcast
from app.routers import sio_game as sio
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload


async def get_log_history(game_id: int, db: Session):
    result = db.execute(
        select(LogMessage)
        .options(selectinload(LogMessage.game))
        .where(LogMessage.game_id == game_id)
        .order_by(LogMessage.created_at)
    )
    return result.scalars().all()
