import asyncio
from sqlalchemy.orm import Session
from app.models.figures import (
    get_figure_by_id,
)
from app.schemas.figures import FigureSchema
from app.services import game_events
from app.services.validate_figure import validate


async def block_figure_service(figures_info : FigureSchema, game_id: int, player_id: int, db: Session):
    if(validate(figures_info, game_id, player_id, db) == 200):
        #Obtiene la figura por su Id
        figure = get_figure_by_id(figures_info.figureCardId, db)
        figure.block = True
        db.commit()
        #emite el evento de bloqueo de figura
        await game_events.emit_block_figure_event(game_id, figure.id)
        return 200

    
