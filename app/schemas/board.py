from pydantic import BaseModel, Field
from typing import List

class PieceResponseSchema(BaseModel):
    squarePieceId: int
    color: str
    row: int
    column: int
