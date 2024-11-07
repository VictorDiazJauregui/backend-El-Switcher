import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.figures import FigureSchema
from app.services.validate_figure import validate, cleanup
from app.services.block_figure import block_figure_service
from app.models.figures import get_figure_by_id
from app.services.board import set_block_color

router = APIRouter()


@router.post("/game/{game_id}/play_figure/{player_id}")
async def validate_figure(
    figures_info: FigureSchema,
    game_id: int,
    player_id: int,
    db: Session = Depends(get_db),
):
    figure = get_figure_by_id(figures_info.figureCardId, db)
    if figure.owner_id == player_id:
        response = validate(figures_info, game_id, player_id, db)
    else:
        response = await block_figure_service(
            figures_info, game_id, player_id, db
        )

    if response == 200:
        set_block_color(game_id, figures_info.colorCards[0].color, db)
        await cleanup(figures_info, game_id, player_id, db)
    return response
