from fastapi import APIRouter
from app.services.game import add_player_to_game
from app.schemas.player import PlayerCreateRequest, PlayerResponseSchema

router = APIRouter()

@router.post("/game/{game_id}/join", response_model=PlayerResponseSchema)
def join_game(game_id: int, player: PlayerCreateRequest):
        response = add_player_to_game(player.name, game_id)
        return response
