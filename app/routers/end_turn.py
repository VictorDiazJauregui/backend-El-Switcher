from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.game import end_turn
from app.db.db import get_db

router = APIRouter()


@router.post("/game/{game_id}/end_turn/{player_id}")
async def end_turn_endpoint(
    game_id: int, player_id: int, db: Session = Depends(get_db)
):
    response = await end_turn(game_id, player_id, db)
    return response
