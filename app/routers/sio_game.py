import socketio

# Create a new Socket.IO server
sio_game = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

@sio_game.on('connect')
async def connect(sid, environ, auth):
    print(f"Client connected: {sid}")