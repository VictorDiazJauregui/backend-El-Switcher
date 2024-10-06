from app.db.db import Player, Game, GameStatus
from app.schemas.player import PlayerResponseSchema, WinnerSchema
from app.models.broadcast import Broadcast
from app.routers import sio_game_list as sio

async def emit_game_list(db):
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

    await sio.emit('game_list', response)

