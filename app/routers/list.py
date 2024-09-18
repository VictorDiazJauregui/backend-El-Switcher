from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.game import get_game_list

router = APIRouter()

@router.get("/game_list")
async def list_endpoint():
    # Fetch the current list of games
    games = get_game_list()
    # Convert the list of games to a format that can be sent over HTTP
    games_list = [game.dict() for game in games]
    # Return the list of games as a JSON response
    return JSONResponse(content={"games": games_list})

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