import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.figures import FigureSchema
from app.services.validate_figure import validate, cleanup
from app.services.block_figure import block_figure_service
from app.models.figures import get_figure_by_id
from app.services.board import set_block_color
from app.services import game_events
from app.services.game_player_service import get_player
from app.services.board import get_blocked_color

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

        player = get_player(player_id, db)
        await game_events.emit_log(
            game_id, f"{player.name} eliminó una de sus figuras.", db
        )
    else:
        response = await block_figure_service(
            figures_info, game_id, player_id, db
        )

    if response == 200:
        await set_block_color(game_id, figures_info.colorCards[0].color, db)
        response = get_blocked_color(game_id, db)
        await game_events.emit_log(
            game_id,
            f"El nuevo color bloqueado es { response['blockedColor'] }.",
            db,
        )
        await cleanup(figures_info, game_id, player_id, db)

    return response
