from app.services.figures import *
from app.schemas.figures import FigureSchema

def validate_figure_function(figures_info: FigureSchema, gameID: int, playerID: int, db : Session):
    """
    Validate the figure of a given player in a game.
    
    Args:
        figures_info (FigureSchema): The figure information.
        gameID (int): The ID of the game.
        playerID (int): The ID of the player.
        db (Session): The database session.

    Returns:
        int: The HTTP status code.
    """
    game = db.query(Game).filter(Game.id == gameID).first()

    if game is None:
        raise ValueError("Game not found")

    player = db.query(Player).filter(Player.id == playerID).first()

    if player is None:
        raise ValueError("Player not found")

    if game.turn != player.turn:
        raise ValueError("Not your turn")

    if game.status != GameStatus.INGAME:
        raise ValueError("Game is not in progress")
    


    return 200