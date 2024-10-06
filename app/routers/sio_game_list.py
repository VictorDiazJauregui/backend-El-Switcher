from app.db.db import db_context, Game, Player, GameStatus
from app.utils.parse_query_string import parse_query_string
from app.models.broadcast import Broadcast
from app.services import lobby_events
import socketio

# Create a new Socket.IO server
sio_game_list = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

@sio_game_list.on('connect')
async def connect(sid):
    print('User connected to game list')

    with db_context() as db:
        await lobby_events.emit_game_list(db)