from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.game import GameCreateSchema, GameListSchema, ListSchema, StartResponseSchema
from app.schemas.player import PlayerResponseSchema
from app.db.db import Game, Player, GameStatus, Turn

def create_game(data: GameCreateSchema, db: Session):
    owner_name = data.ownerName
    game_name = data.gameName
    max_players = data.maxPlayers
    min_players = data.minPlayers

    if not owner_name or not game_name or not max_players or not min_players:
        raise HTTPException(status_code=400, detail="All fields required")
    if max_players < min_players:
        raise HTTPException(status_code=400, detail="maxPlayers must be greater than or equal to minPlayers")
    if min_players < 2 or min_players > 4:
        raise HTTPException(status_code=400, detail="minPlayers must be at least 2 and at most 4")
    if max_players < 2 or max_players > 4:
        raise HTTPException(status_code=400, detail="maxPlayers must be at least 2 and at most 4")

    db_game = Game(
        name=game_name,
        max_players=max_players,
        min_players=min_players,
        status=GameStatus.LOBBY,
        turn=Turn.P2  # default turn is the next player to the host
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    db_player = Player(name=owner_name, game_id=db_game.id, turn=Turn.P1)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return {
        "gameId": db_game.id,
        "ownerId": db_player.id 
    }

from typing import List, Dict

def get_game_list(db: Session) -> List[Dict[str, any]]:
    games = db.query(Game).filter(Game.status == GameStatus.LOBBY).all()
    response = [
        {
            "gameId": game.id,
            "gameName": game.name,
            "connectedPlayers": len(game.players),
            "maxPlayers": game.max_players
        }
        for game in games
    ]
    return response

def get_game(game_id: int, db: Session) -> Game:
    game = db.query(Game).filter(Game.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game with id {game_id} does not exist.")
    return game

def get_player(player_id: int, db: Session) -> Player:
    player = db.query(Player).filter(Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player with id {player_id} does not exist.")
    return player


def add_player_to_game(player_name: str, game_id: int, db: Session) -> PlayerResponseSchema:
    game = get_game(game_id, db)
    
    if game.status != GameStatus.LOBBY: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Game {game_id} is already in progress.")
    
    if len(game.players) >= game.max_players:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Game {game_id} is full.")

    # Determine the turn for the new player
    turn_order = len(game.players) + 1
    turn = Turn(turn_order)

    player = Player(name=player_name, game_id=game.id, turn=turn)
    db.add(player)
    db.commit()
    db.refresh(player)

    return PlayerResponseSchema(
        playerId=player.id,
        name=player.name
    )

def start_game(game_id: int, db: Session) -> StartResponseSchema:
    game = get_game(game_id, db)
    if game.status != GameStatus.LOBBY:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Game {game_id} is already in progress.")
    if game.min_players > len(game.players):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough players to start the game.")

    game.status = GameStatus.INGAME
    db.commit()

    return StartResponseSchema(gameId=game.id, status=game.status)

def end_turn(game_id: int, player_id: int, db: Session):
    game = get_game(game_id, db)
    player = get_player(player_id, db)

    if game.status != GameStatus.INGAME:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Game {game.id} is not in progress.")
    if game.turn != player.turn:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"It's not {player.id} turn.")
    # obtain the current turn value
    current_turn_value = game.turn.value
    # obtain the max turn value
    max_turn_value = len(game.players) +1 #The value starts at 1
    
    # Calculate the next turn value
    next_turn_value = ((current_turn_value + 1) % max_turn_value)

    # If the next turn value is 0, then the next turn is 1
    if next_turn_value == 0:
        next_turn_value = 1
    
    # Assign the new value for turn
    game.turn = Turn(next_turn_value)
    db.commit()
    return {f"Player {player.name} has ended their turn."}
