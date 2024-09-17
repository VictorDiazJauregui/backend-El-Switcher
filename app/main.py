from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import game, websocket

app = FastAPI()

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
app.include_router(websocket.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to The Switcher API"}
