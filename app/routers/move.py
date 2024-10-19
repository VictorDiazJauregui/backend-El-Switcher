from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.move import MakeMoveSchema
from app.db.db import get_db
from app.services.board import make_move

router = APIRouter()


@router.post("/game/{game_id}/move/{player_id}")
async def make_move_endpoint(
    game_id: int,
    player_id: int,
    move_data: MakeMoveSchema,
    db: Session = Depends(get_db),
):
    response = await make_move(game_id, player_id, move_data, db)
    return response
