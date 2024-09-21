from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.game import GameCreateSchema, GameListSchema, ListSchema, StartResponseSchema
from app.schemas.player import PlayerResponseSchema
from app.db.db import Game, Player, GameStatus, Turn, CardMove, CardFig, MoveType, FigureType

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

def add_cards_to_db(db: Session) -> bool: # No se realmente que devolver
    moves = [
        CardMove(id=MoveType.MOV_1.value[0], move=MoveType.MOV_1),
        CardMove(id=MoveType.MOV_2.value[0], move=MoveType.MOV_2),
        CardMove(id=MoveType.MOV_3.value[0], move=MoveType.MOV_3),
        CardMove(id=MoveType.MOV_4.value[0], move=MoveType.MOV_4),
        CardMove(id=MoveType.MOV_5.value[0], move=MoveType.MOV_5),
        CardMove(id=MoveType.MOV_6.value[0], move=MoveType.MOV_6),
        CardMove(id=MoveType.MOV_7.value[0], move=MoveType.MOV_7),
        CardMove(id=MoveType.MOV_8.value[0], move=MoveType.MOV_8),
        CardMove(id=MoveType.MOV_9.value[0], move=MoveType.MOV_9),
        CardMove(id=MoveType.MOV_10.value[0], move=MoveType.MOV_10),
        CardMove(id=MoveType.MOV_11.value[0], move=MoveType.MOV_11),
        CardMove(id=MoveType.MOV_12.value[0], move=MoveType.MOV_12),
        CardMove(id=MoveType.MOV_13.value[0], move=MoveType.MOV_13),
        CardMove(id=MoveType.MOV_14.value[0], move=MoveType.MOV_14),
        CardMove(id=MoveType.MOV_15.value[0], move=MoveType.MOV_15),
        CardMove(id=MoveType.MOV_16.value[0], move=MoveType.MOV_16),
        CardMove(id=MoveType.MOV_17.value[0], move=MoveType.MOV_17),
        CardMove(id=MoveType.MOV_18.value[0], move=MoveType.MOV_18),
        CardMove(id=MoveType.MOV_19.value[0], move=MoveType.MOV_19),
        CardMove(id=MoveType.MOV_20.value[0], move=MoveType.MOV_20),
        CardMove(id=MoveType.MOV_21.value[0], move=MoveType.MOV_21),
        CardMove(id=MoveType.MOV_22.value[0], move=MoveType.MOV_22),
        CardMove(id=MoveType.MOV_23.value[0], move=MoveType.MOV_23),
        CardMove(id=MoveType.MOV_24.value[0], move=MoveType.MOV_24),
        CardMove(id=MoveType.MOV_25.value[0], move=MoveType.MOV_25),
        CardMove(id=MoveType.MOV_26.value[0], move=MoveType.MOV_26),
        CardMove(id=MoveType.MOV_27.value[0], move=MoveType.MOV_27),
        CardMove(id=MoveType.MOV_28.value[0], move=MoveType.MOV_28),
        CardMove(id=MoveType.MOV_29.value[0], move=MoveType.MOV_29),
        CardMove(id=MoveType.MOV_30.value[0], move=MoveType.MOV_30),
        CardMove(id=MoveType.MOV_31.value[0], move=MoveType.MOV_31),
        CardMove(id=MoveType.MOV_32.value[0], move=MoveType.MOV_32),
        CardMove(id=MoveType.MOV_33.value[0], move=MoveType.MOV_33),
        CardMove(id=MoveType.MOV_34.value[0], move=MoveType.MOV_34),
        CardMove(id=MoveType.MOV_35.value[0], move=MoveType.MOV_35),
        CardMove(id=MoveType.MOV_36.value[0], move=MoveType.MOV_36),
        CardMove(id=MoveType.MOV_37.value[0], move=MoveType.MOV_37),
        CardMove(id=MoveType.MOV_38.value[0], move=MoveType.MOV_38),
        CardMove(id=MoveType.MOV_39.value[0], move=MoveType.MOV_39),
        CardMove(id=MoveType.MOV_40.value[0], move=MoveType.MOV_40)
    ]

    figs = [
        CardFig(id=FigureType.EASY_1.value[0], figure=FigureType.EASY_1),
        CardFig(id=FigureType.EASY_2.value[0], figure=FigureType.EASY_2),
        CardFig(id=FigureType.EASY_3.value[0], figure=FigureType.EASY_3),
        CardFig(id=FigureType.EASY_4.value[0], figure=FigureType.EASY_4),
        CardFig(id=FigureType.EASY_5.value[0], figure=FigureType.EASY_5),
        CardFig(id=FigureType.EASY_6.value[0], figure=FigureType.EASY_6),
        CardFig(id=FigureType.EASY_7.value[0], figure=FigureType.EASY_7),
        
        CardFig(id=FigureType.HARD_1.value[0], figure=FigureType.HARD_1),
        CardFig(id=FigureType.HARD_2.value[0], figure=FigureType.HARD_2),
        CardFig(id=FigureType.HARD_3.value[0], figure=FigureType.HARD_3),
        CardFig(id=FigureType.HARD_4.value[0], figure=FigureType.HARD_4),
        CardFig(id=FigureType.HARD_5.value[0], figure=FigureType.HARD_5),
        CardFig(id=FigureType.HARD_6.value[0], figure=FigureType.HARD_6),
        CardFig(id=FigureType.HARD_7.value[0], figure=FigureType.HARD_7),
        CardFig(id=FigureType.HARD_8.value[0], figure=FigureType.HARD_8),
        CardFig(id=FigureType.HARD_9.value[0], figure=FigureType.HARD_9),
        CardFig(id=FigureType.HARD_10.value[0], figure=FigureType.HARD_10),
        CardFig(id=FigureType.HARD_11.value[0], figure=FigureType.HARD_11),
        CardFig(id=FigureType.HARD_12.value[0], figure=FigureType.HARD_12),
        CardFig(id=FigureType.HARD_13.value[0], figure=FigureType.HARD_13),
        CardFig(id=FigureType.HARD_14.value[0], figure=FigureType.HARD_14),
        CardFig(id=FigureType.HARD_15.value[0], figure=FigureType.HARD_15),
        CardFig(id=FigureType.HARD_16.value[0], figure=FigureType.HARD_16),
        CardFig(id=FigureType.HARD_17.value[0], figure=FigureType.HARD_17),
        CardFig(id=FigureType.HARD_18.value[0], figure=FigureType.HARD_18),

        # We need 2 of each card

        CardFig(id=FigureType.EASY_1.value[0], figure=FigureType.EASY_1),
        CardFig(id=FigureType.EASY_2.value[0], figure=FigureType.EASY_2),
        CardFig(id=FigureType.EASY_3.value[0], figure=FigureType.EASY_3),
        CardFig(id=FigureType.EASY_4.value[0], figure=FigureType.EASY_4),
        CardFig(id=FigureType.EASY_5.value[0], figure=FigureType.EASY_5),
        CardFig(id=FigureType.EASY_6.value[0], figure=FigureType.EASY_6),
        CardFig(id=FigureType.EASY_7.value[0], figure=FigureType.EASY_7),
        
        CardFig(id=FigureType.HARD_1.value[0], figure=FigureType.HARD_1),
        CardFig(id=FigureType.HARD_2.value[0], figure=FigureType.HARD_2),
        CardFig(id=FigureType.HARD_3.value[0], figure=FigureType.HARD_3),
        CardFig(id=FigureType.HARD_4.value[0], figure=FigureType.HARD_4),
        CardFig(id=FigureType.HARD_5.value[0], figure=FigureType.HARD_5),
        CardFig(id=FigureType.HARD_6.value[0], figure=FigureType.HARD_6),
        CardFig(id=FigureType.HARD_7.value[0], figure=FigureType.HARD_7),
        CardFig(id=FigureType.HARD_8.value[0], figure=FigureType.HARD_8),
        CardFig(id=FigureType.HARD_9.value[0], figure=FigureType.HARD_9),
        CardFig(id=FigureType.HARD_10.value[0], figure=FigureType.HARD_10),
        CardFig(id=FigureType.HARD_11.value[0], figure=FigureType.HARD_11),
        CardFig(id=FigureType.HARD_12.value[0], figure=FigureType.HARD_12),
        CardFig(id=FigureType.HARD_13.value[0], figure=FigureType.HARD_13),
        CardFig(id=FigureType.HARD_14.value[0], figure=FigureType.HARD_14),
        CardFig(id=FigureType.HARD_15.value[0], figure=FigureType.HARD_15),
        CardFig(id=FigureType.HARD_16.value[0], figure=FigureType.HARD_16),
        CardFig(id=FigureType.HARD_17.value[0], figure=FigureType.HARD_17),
        CardFig(id=FigureType.HARD_18.value[0], figure=FigureType.HARD_18)
    ]

    db.add(moves)
    db.add(figs)



def start_game(game_id: int, db: Session) -> StartResponseSchema:
    game = get_game(game_id, db)
    if game.status != GameStatus.LOBBY:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Game {game_id} is already in progress.")
    if game.min_players > len(game.players):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough players to start the game.")

    game.status = GameStatus.INGAME
    db.commit()

    return StartResponseSchema(gameId=game.id, status=game.status)



def cards_deal(game_id: int, db: Session):
