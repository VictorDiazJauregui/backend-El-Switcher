from fastapi import APIRouter
from app.schemas.game import GameCreateSchema, GameResponseSchema
from app.services.game import create_game

router = APIRouter()

@router.post("/game_create", response_model=GameResponseSchema)
def create_game_endpoint(game_data: GameCreateSchema):
    result = create_game(
        owner_name=game_data.ownerName,
        game_name=game_data.gameName,
        max_players=game_data.maxPlayers,
        min_players=game_data.minPlayers
    )
    return result
