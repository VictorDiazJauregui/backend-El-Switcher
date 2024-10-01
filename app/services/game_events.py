from app.db.db import Player, Game
from app.schemas.player import PlayerResponseSchema
from app.models.broadcast import Broadcast
from app.routers import sio_game as sio

async def emit_players_game(game_id, db):
    players = db.query(Player).filter(Player.game_id == game_id).all()

    #convert every player in player response schema
    PlayerResponseSchemaList = []

    for player in players:
        PlayerResponseSchemaList.append(PlayerResponseSchema(playerId=player.id, playerName=player.name).model_dump())

    broadcast = Broadcast()

    # send the player list to all players in the lobby
    await broadcast.broadcast(sio.sio_game, game_id, 'player_list', PlayerResponseSchemaList)

async def emit_turn_info(game_id, db):
    game = db.query(Game).filter(Game.id == game_id).first()

    player = db.query(Player).filter(Player.game_id == game_id, Player.turn == game.turn).first()

    broadcast = Broadcast()

    turn_info = {
        "playerTurnId": player.id,
    }

    # send the turn info to all players in the lobby
    await broadcast.broadcast(sio.sio_game, game_id, 'turn', turn_info)