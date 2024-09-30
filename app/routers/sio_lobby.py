from app.utils.parse_query_string import parse_query_string
import socketio

# Create a new Socket.IO server
sio_lobby = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

@sio_lobby.on('connect')
async def connect(sid, environ, auth):
    player_id, game_id = parse_query_string(environ)

    print(f'Player {player_id} connected to lobby {game_id}')

