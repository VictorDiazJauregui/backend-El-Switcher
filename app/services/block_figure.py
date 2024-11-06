import asyncio
from app.db.db import Game, GameStatus, Player
from app.models.figures import (
    get_figure_by_id,
    get_figure_type_by_id,
    select_figure_by_his_type,
)
from app.schemas.figures import FigureSchema
from app.services import game_events
from app.services.board import delete_partial_cache, set_block_color
from app.services.cards import (
    delete_figure_card,
    unassign_played_movement_cards,
)
from app.services.figures import *
from app.services.validate_figure import validate


async def block_figure_service(figures_info : FigureSchema, game_id: int, player_id: int, db: Session):
    if(validate(figures_info, game_id, player_id, db) == 200):
        #Obtiene la figura por su Id
        figure = get_figure_by_id(figures_info.figureCardId, db)
        figure.block = True
        db.commit()
        #emite el evento de bloqueo de figura
        await game_events.emit_block_figure_event(game_id, figure.id)

    
