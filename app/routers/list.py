from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services.game import get_game_list

router = APIRouter()

@router.get("/game_list")
def list_endpoint(db: Session = Depends(get_db)):
    print("test1")
    # Fetch the current list of games
    games = get_game_list(db)
    # Convert the list of games to a format that can be sent over HTTP
    print("test2")
    return games

'''
from fastapi import APIRouter, WebSocket
from typing import List
from app.services.game import get_game_list

router = APIRouter()

@router.websocket("/game_list")
async def list_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Fetch the current list of games
        games = get_game_list()
        # Convert the list of games to a format that can be sent over WebSocket
        games_list = [game.dict() for game in games]
        # Send the list of games to the client
        await websocket.send_json({"games": games_list})
'''