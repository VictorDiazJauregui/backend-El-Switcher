from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.services.game import remove_player_from_game

router = APIRouter()


@router.delete("/game/{game_id}/leave/{player_id}")
async def leave_game(
    game_id: int, player_id: int, db: Session = Depends(get_db)
):
    response = await remove_player_from_game(game_id, player_id, db)
    return response
