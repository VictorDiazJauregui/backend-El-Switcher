from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.game import StartResponseSchema
from app.services.board import create_board
from app.services.cards import add_cards_to_db, initialize_cards
from app.services.game import start_game

router = APIRouter()


@router.post("/game/{game_id}/start", response_model=StartResponseSchema)
async def start(game_id: int, db: Session = Depends(get_db)):
    response = await start_game(game_id, db)
    create_board(game_id, db)
    add_cards_to_db(game_id, db)
    initialize_cards(game_id, db)

    return response
