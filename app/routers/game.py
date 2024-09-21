from fastapi import APIRouter, Depends
from app.schemas.game import GameCreateSchema, GameResponseSchema
from app.services.game import create_game
from sqlalchemy.orm import Session
from app.db.db import get_db


router = APIRouter()

@router.post("/game_create", response_model=GameResponseSchema)
def create_game_endpoint(game_data: GameCreateSchema, db: Session = Depends(get_db)):
    response = create_game(game_data, db)
    return response

###--------------------------------------------------------------------------------
# No se
from fastapi import WebSocket

@router.websocket("/game/{gameID}/ws")
async def run_game(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    while True:
        if(db.query)