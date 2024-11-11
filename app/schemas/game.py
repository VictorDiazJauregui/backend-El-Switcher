from pydantic import BaseModel
from typing import List


class GameCreateSchema(BaseModel):
    ownerName: str
    gameName: str
    password: str = None
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


class GameInfoSchema(BaseModel):
    gameId: int
    gameName: str
    maxPlayers: int
    minPlayers: int
    status: str
