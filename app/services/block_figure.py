import asyncio
from sqlalchemy.orm import Session
from app.models.figures import (
    get_figure_by_id,
)
from app.schemas.figures import FigureSchema
from app.services.validate_figure import validate
from app.db.db import CardFig


async def block_figure_service(
    figures_info: FigureSchema, game_id: int, player_id: int, db: Session
):
    if validate(figures_info, game_id, player_id, db) == 200:
        # Obtiene la figura por su Id
        figure = get_figure_by_id(figures_info.figureCardId, db)
        # verifico que el resto de la mano del jugador no esté bloqueada

        len_card_figs_from_player_blocked = len(
            db.query(CardFig)
            .filter(
                CardFig.game_id == figure.game_id,
                CardFig.owner_id == figure.owner_id,
                CardFig.in_hand == True,
                CardFig.block == True,
            )
            .all()
        )

        if len_card_figs_from_player_blocked >= 1:
            raise ValueError("The player already has a blocked figure")

        len_card_figs_from_player = len(
            db.query(CardFig)
            .filter(
                CardFig.game_id == figure.game_id,
                CardFig.owner_id == figure.owner_id,
                CardFig.in_hand == True,
            )
            .all()
        )
        if len_card_figs_from_player < 2:
            raise ValueError(
                "You can't block a figure from a player that has less than 2 figures in hand"
            )

        # Bloquea la figura
        figure.block = True
        db.commit()
        return 200
