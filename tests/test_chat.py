import pytest
from app.db.db import GameStatus
from app.schemas.chat import ChatMessageSchema
from app.services.chat import get_chat_history
from .db_setup import (
    client,
    TestingSessionLocal,
    reset_db,
    create_game,
    create_player,
)


@pytest.fixture(scope="module")
def test_client():
    yield client


reset_db()


def test_chat_ingame(test_client):
    db = TestingSessionLocal()
    # First, create a game
    game = create_game(db, GameStatus.INGAME)
    player = create_player(db, game.id)

    # Delete player from the lobby
    response = test_client.post(
        f"/game/{game.id}/send_message",
        json={
            "playerId": player.id,
            "message": "HOLA SE ESCUCHA",
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_chat_history():
    db = TestingSessionLocal()

    chat_history = await get_chat_history(game_id=1, db=db)

    assert chat_history[0].message == "HOLA SE ESCUCHA"
    assert len(chat_history) == 1
