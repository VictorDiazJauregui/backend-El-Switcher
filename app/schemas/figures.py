from pydantic import BaseModel, Field
from typing import List


class SimplePieceSchema(BaseModel):
    color: str
    row: int
    column: int


class FigureSchema(BaseModel):
    figureCardId: int
    colorCards: List[SimplePieceSchema]
