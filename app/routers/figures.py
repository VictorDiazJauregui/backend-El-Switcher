from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.figures import figures_event

router = APIRouter()


# responde con una matriz de colores
@router.get("/game/{game_id}/figures")
def figures(game_id: int, db: Session = Depends(get_db)):
    """
    Retrieve figures for a given game.

    Args:
        game_id (int): The ID of the game.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the figures.
    """

    response = figures_event(game_id, db)

    return response
