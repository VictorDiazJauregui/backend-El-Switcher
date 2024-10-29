from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.figures import FigureSchema
from app.services.validate_figure import validate, cleanup

router = APIRouter()

@router.post("/game/{game_id}/play_figure/{player_id}")
async def validate_figure(
    figures_info: FigureSchema,
    game_id: int,
    player_id: int,
    db: Session = Depends(get_db)):

    response = validate(figures_info, game_id, player_id, db)
    if response == 200:
        await cleanup(figures_info, game_id, player_id, db)
    return response