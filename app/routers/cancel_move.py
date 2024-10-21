from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.board import validate_and_cancel_move

from app.db.db import get_db

router = APIRouter()


@router.post("/game/{game_id}/move_undo/{player_id}")
async def cancel_move_endpoint(
    game_id: int, player_id: int, db: Session = Depends(get_db)
):
    response = await validate_and_cancel_move(game_id, player_id, db)
    return response
