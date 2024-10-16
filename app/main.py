from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.db import Base, engine
import socketio

from app.routers import game, join, start, end_turn, leave, move, figures, cancel_move
from app.routers.sio_game import sio_game
from app.routers.sio_lobby import sio_lobby
from app.routers.sio_game_list import sio_game_list
from app.errors.handlers import value_error_handler, runtime_error_handler, generic_exception_handler, validation_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# Register error handlers
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RuntimeError, runtime_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# CORS configuration
# Configuración no implementada, ejemplo:
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dominio.com",  # Permite solo tu dominio principal
                                # Agregar subdominios correspondientes
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Permite solo métodos necesarios
    allow_headers=["Content-Type", "Authorization"],  # Permite solo encabezados necesarios
    
    # En producción, especifica solo los encabezados que tu API necesita aceptar.
)
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Especifica qué dominios están permitidos para hacer solicitudes a tu servidor.
    allow_credentials=True, # Permite el envío de credenciales (como cookies) en las solicitudes CORS.
    allow_methods=["*"],  # Especifica qué métodos HTTP están permitidos para solicitudes CORS ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],  # Especifica qué encabezados pueden ser enviados en solicitudes CORS. (Content-Type, Authorization, etc.)
)

# No es necesario cargar ni guardar ningún estado, ya que no hay persistencia

app.include_router(game.router)
app.include_router(join.router)
app.include_router(start.router)
app.include_router(end_turn.router)
app.include_router(leave.router)
app.include_router(move.router)
# Register the figures router
app.include_router(figures.router)
app.include_router(cancel_move.router)

# Mount the Socket.IO app
socket_app = socketio.ASGIApp(sio_game, other_asgi_app=app, socketio_path="/game/ws")
app.mount("/game/ws", socket_app)

socket_app = socketio.ASGIApp(sio_lobby, other_asgi_app=app, socketio_path="/game/lobby/ws")
app.mount("/game/lobby/ws", socket_app)

socket_app = socketio.ASGIApp(sio_game_list, other_asgi_app=app, socketio_path="/game_list/ws")
app.mount("/game_list/ws", socket_app)

@app.get("/")
def read_root():
    return {"message": "Welcome to The Switcher API"}
