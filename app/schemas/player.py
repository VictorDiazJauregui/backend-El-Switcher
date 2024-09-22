from pydantic import BaseModel

class PlayerCreateRequest(BaseModel):
    playerName: str

class PlayerResponseSchema(BaseModel):
    playerId: int
    playerName: str
