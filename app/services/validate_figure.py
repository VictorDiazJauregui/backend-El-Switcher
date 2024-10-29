from app.db.db import Game, GameStatus, Player
from app.models.figures import (
    get_figure_by_id,
    get_figure_type_by_id,
    select_figure_by_his_type,
)
from app.schemas.figures import FigureSchema
from app.services import game_events
from app.services.board import delete_partial_cache
from app.services.cards import (
    delete_figure_card,
    unassign_played_movement_cards,
)
from app.services.figures import *


def game_checks(game: Game):
    if game is None:
        raise ValueError("Game not found")
    if game.status != GameStatus.INGAME:
        raise ValueError("Game is not in progress")


def player_checks(player: Player, game: Game):
    if player is None:
        raise ValueError("Player not found")
    if player.game_id != game.id:
        raise ValueError("Player does not belong to game")
    if player.turn != game.turn:
        raise ValueError("Not your turn")


def component_checks(components):
    if len(components) == 0:
        raise ValueError("No connected components found")
    elif len(components) > 1:
        raise ValueError("More than one connected component found")


def process_components(figures_info):
    matrix = np.full((6, 6), None, dtype=object)
    colorCards = [card.model_dump() for card in figures_info.colorCards]

    for figure in colorCards:
        matrix[figure["row"]][figure["column"]] = figure["color"]

    components = find_connected_components(matrix, colorCards[0]["color"])

    component_checks(components)

    return components


def figure_checks(figures_info, components, db):
    cardId = figures_info.figureCardId

    figure = get_figure_by_id(cardId, db)
    if figure is None:
        raise ValueError("Figure not found")

    figure_type = get_figure_type_by_id(cardId, db)
    if figure_type is None:
        raise ValueError("Figure type not found")

    selected_figure = select_figure_by_his_type(figure_type.value[1])
    if not selected_figure.matches_any_rotation(components[0]):
        raise ValueError("Figure does not match connected component")


def validate(
    figures_info: FigureSchema, gameID: int, playerID: int, db: Session
):

    game = db.query(Game).filter(Game.id == gameID).first()
    game_checks(game)

    player = db.query(Player).filter(Player.id == playerID).first()
    player_checks(player, game)

    components = process_components(figures_info)

    figure_checks(figures_info, components, db)

    return 200


async def cleanup(figures_info, game_id, player_id, db):
    delete_partial_cache(game_id, db)
    delete_figure_card(figures_info.figureCardId, db)
    unassign_played_movement_cards(player_id, db)
    await game_events.emit_cards(game_id, player_id, db)
