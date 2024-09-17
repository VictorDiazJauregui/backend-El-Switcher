import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from app.main import app  # Asegúrate de importar tu aplicación FastAPI aquí

@pytest.mark.asyncio
async def test_create_and_join_game():
    transport = ASGITransport(app=app)  # Usamos ASGITransport explícitamente
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Paso 1: Crear el juego
        response = await client.post("/game_create", json={
            "ownerName": "Alice",
            "gameName": "Test Game",
            "maxPlayers": 4,
            "minPlayers": 2
        })
        assert response.status_code == 200
        response_data = response.json()
        game_id = response_data["gameId"]

        # Paso 2: Unir jugadores
        player_names = ["Charlie", "David", "Bob"]
        for player_name in player_names:
            response = await client.post(f"/game/{game_id}/join", json={"name": player_name})
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["name"] == player_name

        # Intentar agregar un jugador extra y verificar el error
        response = await client.post(f"/game/{game_id}/join", json={"name": "Eve"})
        assert response.status_code == 400  # Esperamos un error 400 ya que el juego está lleno
        assert response.json()["detail"] == f"Game {game_id} is full."