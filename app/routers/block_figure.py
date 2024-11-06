from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.block_figure import block_figure_service
from app.schemas.figures import FigureSchema

from app.db.db import get_db

router = APIRouter()

@router.post("/game/{gameID}/block_figure/{playerID}")
async def block_figure_endpoint(
    figures_info: FigureSchema,
    gameId: int,
    playerId: int,
    db: Session = Depends(get_db),
):
    response = await block_figure_service(figures_info, gameId, playerId, db)
    return response