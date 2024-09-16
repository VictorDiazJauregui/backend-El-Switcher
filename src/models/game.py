from pydantic import BaseModel
from typing import List

class Game(BaseModel):
    gameId: int
    gameName: str
    maxPlayers: int
    players: List[str]