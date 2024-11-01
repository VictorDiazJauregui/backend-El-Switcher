from app.db.db import Game, GameStatus
from app.routers import sio_game_list as sio


async def emit_game_list(db):
    games = db.query(Game).filter(Game.status == GameStatus.LOBBY).all()
    response = [
        {
            "gameId": game.id,
            "gameName": game.name,
            "connectedPlayers": len(game.players),
            "maxPlayers": game.max_players,
            "isPublic": game.password is None,
        }
        for game in games
    ]

    await sio.sio_game_list.emit("game_list", response)
