from fastapi import APIRouter, Depends
from app.schemas.move import MakeMoveSchema
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services.board import make_move

router = APIRouter()

@router.post("/game/{game_id}/move")
async def make_move_endpoint(move_data: MakeMoveSchema, db: Session = Depends(get_db)):
    response = await make_move(move_data, db)
    return response