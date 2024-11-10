from app.db.db import LogMessage
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload


async def get_log_history(game_id: int, db: Session):
    result = db.execute(
        select(LogMessage)
        .where(LogMessage.game_id == game_id)
        .order_by(LogMessage.created_at)
    )
    return result.scalars().all()
