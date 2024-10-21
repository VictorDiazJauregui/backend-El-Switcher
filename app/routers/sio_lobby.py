import socketio

from app.db.db import db_context, Game, Player, GameStatus
from app.models.broadcast import Broadcast
from app.services import lobby_events
from app.utils.parse_query_string import parse_query_string

# Create a new Socket.IO server
sio_lobby = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])


@sio_lobby.on("connect")
async def connect(sid, environ, auth):
    player_id, game_id = parse_query_string(environ)

    print(f"Player {player_id} connected to lobby {game_id}")

    with db_context() as db:
        game = db.query(Game).filter(Game.id == game_id).first()

        if game is None:
            print(f"Game {game_id} does not exist")
            return  # Game does not exist, then disconnect the player

        if game.status != GameStatus.LOBBY:
            print(f"Game {game_id} is not in lobby status")
            return  # Game is not in lobby status, then disconnect the player

        # check if the player is part of the game
        player = (
            db.query(Player).filter_by(id=player_id, game_id=game.id).first()
        )

        if player is None:
            print(f"Player {player_id} is not part of game {game_id}")
            return  # Player is not part of the game, then disconnect the player

        # Register the player's socket
        broadcast = Broadcast()

        await broadcast.register_player_socket(
            sio_lobby, player_id, game_id, sid
        )

        await lobby_events.emit_players_lobby(game_id, db)

        await lobby_events.emit_can_start_game(game_id, db)
