from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.routers import game, list, join
from app.errors.handlers import value_error_handler, generic_exception_handler, validation_exception_handler
app = FastAPI()

# Register error handlers
app.add_exception_handler(ValueError, value_error_handler)
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
app.include_router(list.router)
app.include_router(join.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to The Switcher API"}
