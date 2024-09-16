from fastapi import FastAPI
from app.routers import game

app = FastAPI()

# No es necesario cargar ni guardar ningún estado, ya que no hay persistencia

app.include_router(game.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to The Switcher API"}
