import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from app.main import app  # Asegúrate de importar tu aplicación FastAPI aquí

@pytest.mark.asyncio
async def test_create_join_and_start_game():
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

        # Intentar iniciar el juego con menos del número mínimo de jugadores (2)
        response = await client.post(f"/game/{game_id}/start")
        assert response.status_code == 404  # Esperamos un error ya que no hay suficientes jugadores
        assert response.json()["detail"] == "Not enough players to start the game."

        # Paso 2: Unir jugadores al juego
        player_names = ["Bob", "Charlie"]
        for player_name in player_names:
            response = await client.post(f"/game/{game_id}/join", json={"name": player_name})
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["name"] == player_name

        # Intentar iniciar el juego con el número mínimo de jugadores (2)
        response = await client.post(f"/game/{game_id}/start")
        assert response.status_code == 200  # El juego debería empezar correctamente
        response_data = response.json()
        assert response_data["status"] == "ingame"  # Verificamos que el estado del juego cambió a 'ingame'

        # Paso 3: Intentar unirse a un juego que ya está en progreso
        response = await client.post(f"/game/{game_id}/join", json={"name": "David"})
        assert response.status_code == 400  # Esperamos un error ya que el juego no está en "lobby"
        assert response.json()["detail"] == f"Game {game_id} is already in progress."

        # Intentar iniciar el juego nuevamente (una vez iniciado, no se puede volver a iniciar)
        response = await client.post(f"/game/{game_id}/start")
        assert response.status_code == 400  # No se debería poder reiniciar un juego ya iniciado
        assert response.json()["detail"] == f"Game {game_id} is already in progress."