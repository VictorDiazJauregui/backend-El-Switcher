from pydantic import BaseModel, Field
from typing import List
from app.db.db import FigureType

class CardFigSchema(BaseModel):
    figureCardId: int
    difficulty: str
    figureType: int

class CardFigResponseSchema(BaseModel):
    ownerId: int
    cards: List[CardFigSchema]

class CardMoveResponseSchema(BaseModel):
    movementcardId: int
    type: str