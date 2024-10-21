from pydantic import BaseModel


class MakeMoveSchema(BaseModel):
    movementCardId: int
    squarePieceId1: int
    squarePieceId2: int
