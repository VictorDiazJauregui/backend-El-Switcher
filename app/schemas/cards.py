from pydantic import BaseModel
from typing import List


class CardFigSchema(BaseModel):
    figureCardId: int
    difficulty: str
    figureType: int
    isBlocked: bool


class CardFigResponseSchema(BaseModel):
    ownerId: int
    cards: List[CardFigSchema]


class CardMoveResponseSchema(BaseModel):
    movementcardId: int
    type: str
    moveType: int
    played: bool
