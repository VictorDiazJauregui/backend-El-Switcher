from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services.game import get_game_list

router = APIRouter()

@router.get("/game_list")
def list_endpoint(db: Session = Depends(get_db)):
    # Fetch the current list of games
    games = get_game_list(db)
    # Convert the list of games to a format that can be sent over HTTP
    return games
