"""Module providing the player class"""
from pydantic import BaseModel

class Player(BaseModel):
    """Class representing a player in the game"""
    id: int
    name: str
    
