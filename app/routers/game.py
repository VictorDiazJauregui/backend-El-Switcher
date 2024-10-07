from fastapi import APIRouter, Depends
from app.schemas.game import GameCreateSchema, GameResponseSchema, GameInfoSchema
from app.services.game import create_game, get_game
from app.services.board import create_board
from sqlalchemy.orm import Session
from app.db.db import get_db

router = APIRouter()

@router.post("/game_create", response_model=GameResponseSchema)
async def create_game_endpoint(game_data: GameCreateSchema, db: Session = Depends(get_db)):
    response = await create_game(game_data, db)
    create_board(response["gameId"], db)

    return response

@router.get("/game/{gameID}")
def get_game_by_id(gameID: int, db: Session = Depends(get_db)):
    game = get_game(gameID, db)
    
    return GameInfoSchema(
        gameId=game.id, 
        gameName=game.name, 
        maxPlayers=game.max_players, 
        minPlayers=game.min_players
    )