import json
import pytest
import websockets
import asyncio

@pytest.mark.asyncio
async def test_websocket_game_list():
    uri = "ws://127.0.0.1:8000/game_list"

    async with websockets.connect(uri) as websocket:
        # Fetch the initial list of games
        response = await websocket.recv()
        response = json.loads(response)  # Parse JSON response
        
        assert "games" in response
        assert isinstance(response["games"], list)  # Verify that "games" is a list

        # Example: After receiving one message, close connection to prevent infinite loop
        await websocket.close()  # Close WebSocket connection