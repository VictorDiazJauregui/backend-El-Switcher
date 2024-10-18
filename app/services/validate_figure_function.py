from app.services.figures import *
from app.schemas.figures import FigureSchema
from app.models.figures import get_figure_by_id, get_figure_type_by_id, select_figure_by_his_type 
from app.db.db import Game, GameStatus, Player


def validate_figure_function(figures_info: FigureSchema, gameID: int, playerID: int, db : Session) :
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
    
    #convertir figures_info a una lista con los atributos de FigureSchema
    colorCards = []
    for colorCard in figures_info.colorCards:
        colorCards.append(colorCard.model_dump())
    
    matrix = np.full((6, 6), None, dtype=object)

    # Iteramos sobre los diccionarios en colorCards
    for figure in colorCards:
    # Accedemos a los valores como un diccionario, no como atributos de un objeto
        matrix[figure['row']][figure['column']] = figure['color']


    connected_components = find_connected_components(matrix, colorCards[0]['color'])

    
    if len(connected_components) == 0:
        raise ValueError("No connected components found")
    elif len(connected_components) > 1:
        raise ValueError("More than one connected component found")
    
    
    cardId = figures_info.figureCardId

    figure = get_figure_by_id(cardId, db)
    if figure is None:
        raise ValueError("Figure not found")
    
    figure_type = get_figure_type_by_id(cardId, db)



    if figure_type is None:
        raise ValueError("Figure type not found")

    selected_figure = select_figure_by_his_type(figure_type.value[1])

    
    if not selected_figure.matches_any_rotation(connected_components[0]):
        raise ValueError("Figure does not match connected component")
    return 200