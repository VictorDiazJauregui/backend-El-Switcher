from pydantic import BaseModel, Field
from typing import List

class MakeMoveSchema(BaseModel):
    movementCardId: int
    squarePieceId1: int
    squarePieceId2: int