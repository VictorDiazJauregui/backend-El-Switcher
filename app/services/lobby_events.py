from app.db.db import Player, Game, Turn
from app.models.broadcast import Broadcast
from app.routers import sio_lobby as sio
from app.schemas.player import PlayerResponseSchema


async def emit_players_lobby(game_id, db):
    players = db.query(Player).filter(Player.game_id == game_id).all()

    # convert every player in player response schema
    PlayerResponseSchemaList = []

    for player in players:
        PlayerResponseSchemaList.append(
            PlayerResponseSchema(
                playerId=player.id, playerName=player.name
            ).model_dump()
        )

    broadcast = Broadcast()

    # send the player list to all players in the lobby
    await broadcast.broadcast(
        sio.sio_lobby, game_id, "player_list", PlayerResponseSchemaList
    )


async def emit_can_start_game(game_id, db):
    game = db.query(Game).filter(Game.id == game_id).first()

    players = db.query(Player).filter(Player.game_id == game_id).all()

    # Check if the game can start
    can_start = (
        len(players) >= game.min_players and len(players) <= game.max_players
    )

    # Get the owner of the game
    owner_id = [player.id for player in players if player.turn == Turn.P1][0]

    broadcast = Broadcast()

    # Send that the game can start to the owner
    await broadcast.send_to_player(
        sio.sio_lobby, owner_id, "start_game", {"canStart": can_start}
    )


async def emit_game_started(game_id):
    broadcast = Broadcast()

    # Send that the game has started to all players in the lobby
    await broadcast.broadcast(
        sio.sio_lobby, game_id, "game_started", {"gameStarted": True}
    )


async def emit_game_cancel(game_id):
    broadcast = Broadcast()

    await broadcast.broadcast(
        sio.sio_lobby, game_id, "cancel_game", {"gameCanceled": True}
    )
