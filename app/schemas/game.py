from pydantic import BaseModel, Field
from typing import List

class GameCreateSchema(BaseModel):
    ownerName: str
    gameName: str
    maxPlayers: int

class GameResponseSchema(BaseModel):
    gameId: int
    gameName: str
    maxPlayers: int
    players: List[str]