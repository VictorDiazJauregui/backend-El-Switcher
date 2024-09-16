from pydantic import BaseModel, Field
from typing import List

class GameCreateSchema(BaseModel):
    ownerName: str
    gameName: str
    maxPlayers: int
    minPlayers: int

class GameResponseSchema(BaseModel):
    gameId: int
    ownerId: int