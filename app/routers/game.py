from fastapi import APIRouter, Depends
from app.schemas.game import GameCreateSchema, GameResponseSchema
from app.services.game import create_game
from app.services.board import create_board
from sqlalchemy.orm import Session
from app.db.db import get_db

router = APIRouter()

@router.post("/game_create", response_model=GameResponseSchema)
async def create_game_endpoint(game_data: GameCreateSchema, db: Session = Depends(get_db)):
    response = create_game(game_data, db)
    create_board(response["gameId"], db)

    return response