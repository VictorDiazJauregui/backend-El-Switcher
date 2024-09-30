from pydantic import BaseModel, Field
from typing import List

class CardFigSchema(BaseModel):
    figureCardId: int
    difficulty: str

class CardFigResponseSchema(BaseModel):
    ownerId: int
    cards: List[CardFigSchema]

class CardMoveResponseSchema(BaseModel):
    movementcardId: int
    type: str