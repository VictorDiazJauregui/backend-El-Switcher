"""Module providing the game class"""

from pydantic import BaseModel


class Game(BaseModel):
    """Class representing a game"""
    id: int
    name: str
    max_players: int
