from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.figures import figures_event
from app.db.db import Color, get_db
from fastapi.encoders import jsonable_encoder
from app.schemas.figures import FigureSchema
from app.services.validate_figure_function import validate_figure_function
import numpy as np


router = APIRouter()


@router.post("/game/{game_id}/play_figure/{player_id}")
def validate_figure(figures_info: FigureSchema,
                    game_id: int, player_id: int,
                    db: Session = Depends(get_db)):
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

   
    response = validate_figure_function(figures_info, game_id, player_id, db)
    print(response)
    return response

