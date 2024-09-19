from pydantic import BaseModel

class PlayerCreateRequest(BaseModel):
    name: str

class PlayerResponseSchema(BaseModel):
    playerId: int
    name: str
