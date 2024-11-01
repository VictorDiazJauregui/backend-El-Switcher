from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.figures import FigureSchema
from app.services.validate_figure_function import validate_figure_function
from app.services.cards import (
    delete_figure_card,
    unassign_played_movement_cards,
)
from app.services import game_events
from app.services.board import delete_partial_cache


router = APIRouter()


@router.post("/game/{game_id}/play_figure/{player_id}")
async def validate_figure(
    figures_info: FigureSchema,
    game_id: int,
    player_id: int,
    db: Session = Depends(get_db),
):
    """
    Validate the figure of a given player in a game.

    Args:
        gameID (int): The ID of the game.
        playerID (int): The ID of the player.
        db (Session): The database session.

    Returns:
        int: The HTTP status code.
        details: The details of the response, if exists.
    """

    response = await validate_figure_function(figures_info, game_id, player_id, db)
    if response == 200:
        delete_partial_cache(game_id, db)
        delete_figure_card(figures_info.figureCardId, db)
        unassign_played_movement_cards(player_id, db)
        await game_events.emit_cards(game_id, player_id, db)

    print(response)
    return response
