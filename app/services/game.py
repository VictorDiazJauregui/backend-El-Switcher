from fastapi import HTTPException
from typing import Dict, List
from app.models.game import Game
from app.schemas.game import GameListSchema

games: Dict[int, Game] = {}  # Dictionary to store games
game_id_counter = 1

def create_game(owner_name: str, game_name: str, max_players: int, min_players: int) -> Game:
    global game_id_counter

    if not owner_name or not game_name or not max_players or not min_players:
        raise HTTPException(status_code=400, detail="All fields required")
    if max_players < min_players:
        raise HTTPException(status_code=400, detail="maxPlayers must be greater than or equal to minPlayers")
    if min_players < 2 or min_players > 4:
        raise HTTPException(status_code=400, detail="minPlayers must be at least 2 and at most 4")
    if max_players < 2 or max_players > 4:
        raise HTTPException(status_code=400, detail="maxPlayers must be at least 2 and at most 4")

    new_game = Game(
        gameId=game_id_counter,
        gameName=game_name,
        maxPlayers=max_players,
        minPlayers=min_players,
        players=[owner_name],  # Add the host as the first player
        status="lobby", # default status is lobby, other status: playing, finished.
        turn=1 # default turn is the next player to the host
    )
    games[game_id_counter] = new_game # Add the game to the dictionary
    game_id_counter += 1 # Increment the game ID counter
    return {
        "gameId": new_game.gameId,
        "ownerId": 0  # The owner is always the first player in the list
    }

def get_game_list() -> List[GameListSchema]: # Return a list of games in a format that can be sent over WebSocket
    return [GameListSchema(
        gameId=game.gameId,
        gameName=game.gameName,
        connectedPlayers=len(game.players),
        maxPlayers=game.maxPlayers
    ) for game in games.values()]

def get_game(game_id: int) -> Game:
    return games.get(game_id)  # Return the game if found, otherwise None