from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services.game import remove_player_from_game

router = APIRouter()

@router.delete("game/{gameID}/leave/{playerID}")
def leave_game(gameID: int, playerID: int, db: Session = Depends(get_db)):
    response = remove_player_from_game(gameID, playerID, db)
    return response