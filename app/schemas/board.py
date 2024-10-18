from pydantic import BaseModel

class PieceResponseSchema(BaseModel):
    squarePieceId: int
    color: str
    row: int
    column: int
