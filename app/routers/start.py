from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.game import StartResponseSchema
from app.db.db import get_db
from app.services.game import start_game

router = APIRouter()

@router.post("/game/{game_id}/start", response_model=StartResponseSchema)
def start(game_id: int, db: Session = Depends(get_db)):
        response = start_game(game_id, db)
        return response