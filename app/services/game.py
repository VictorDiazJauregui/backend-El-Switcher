from fastapi import HTTPException
from typing import Dict
from app.models.game import Game

games: Dict[int, Game] = {}  # Dictionary to store games
game_id_counter = 1

def create_game(owner_name: str, game_name: str, max_players: int, min_players: int) -> Game:
    global game_id_counter

    if not owner_name or not game_name or not max_players or not min_players:
        raise HTTPException(status_code=400, detail="All fields required")
    if max_players < 2:
        raise HTTPException(status_code=400, detail="maxPlayers must be at least 2")
    if max_players > 4:
        raise HTTPException(status_code=400, detail="maxPlayers must be at most 4")

    new_game = Game(
        gameId=game_id_counter,
        gameName=game_name,
        maxPlayers=max_players,
        players=[owner_name]  # Add the host as the first player
    )
    games[game_id_counter] = new_game
    game_id_counter += 1
    return {
        "gameId": new_game.gameId,
        "ownerId": 0  # The owner is always the first player in the list
    }

def get_game(game_id: int) -> Game:
    return games.get(game_id)  # Return the game if found, otherwise None