from pydantic import BaseModel


class PlayerCreateRequest(BaseModel):
    playerName: str
    password: str = None


class PlayerResponseSchema(BaseModel):
    playerId: int
    playerName: str


class WinnerSchema(BaseModel):
    idWinner: int
    nameWinner: str
