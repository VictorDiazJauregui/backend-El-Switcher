import socketio

from app.db.db import db_context
from app.services import game_list_events

# Create a new Socket.IO server
sio_game_list = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins=[]
)


@sio_game_list.on("connect")
async def connect(sid, environ, auth):
    print("User connected to game list")

    with db_context() as db:
        await game_list_events.emit_game_list(db)
