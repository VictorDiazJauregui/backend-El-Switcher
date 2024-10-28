from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.player import PlayerCreateRequest, PlayerResponseSchema
from app.db.db import get_db
from app.services.game import add_player_to_game

router = APIRouter()


@router.post("/game/{game_id}/join", response_model=PlayerResponseSchema)
async def join_game(
    game_id: int, player: PlayerCreateRequest, db: Session = Depends(get_db)
):
    response = await add_player_to_game(
        player.playerName, game_id, db, player.password
    )

    return response
