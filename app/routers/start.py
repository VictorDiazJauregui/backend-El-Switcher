from fastapi import APIRouter
from app.services.game import start_game
from app.schemas.game import StartResponseSchema

router = APIRouter()

@router.post("/game/{game_id}/start", response_model=StartResponseSchema)
def start(game_id: int):
        response = start_game(game_id)
        return response