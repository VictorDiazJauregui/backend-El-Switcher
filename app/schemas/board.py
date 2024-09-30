from pydantic import BaseModel, Field
from typing import List

class PieceResponseSchema(BaseModel):
    color: str
    row: int
    column: int
