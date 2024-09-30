from app.db.db import db_context, Game, Player
from app.utils.parse_query_string import parse_query_string
from app.models.broadcast import Broadcast
import socketio

# Create a new Socket.IO server
sio_game = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

@sio_game.on('connect')
async def connect(sid, environ, auth):
    player_id, game_id = parse_query_string(environ)

    print(f'Player {player_id} connected to game {game_id}')
    
    with db_context() as db:
        game = db.query(Game).filter(Game.id == game_id).first()
        if game is None:
            print(f'Game {game_id} does not exist')
            return # Game does not exist, then disconnect the player
        
        # check if the player is part of the game
        player = db.query(Player).filter_by(id=player_id, game_id=game.id).first()
        if player is None:
            print(f'Player {player_id} is not part of game {game_id}')
            return # Player is not part of the game, then disconnect the player

        # Register the player's socket
        broadcast = Broadcast()
        
        await broadcast.register_player_socket(sio_game, player_id, game_id, sid)
        
        await broadcast.broadcast(sio_game, game_id, 'player_connected', {'playerId': player_id, 'playerName': player.name})
