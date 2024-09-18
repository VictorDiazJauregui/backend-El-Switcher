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

class GameListSchema(BaseModel):
    gameId: int
    gameName: str
    connectedPlayers: int
    maxPlayers: int

class ListSchema(BaseModel):
    games: List[GameListSchema]

class StartResponseSchema(BaseModel):
    gameId: int
    status: str