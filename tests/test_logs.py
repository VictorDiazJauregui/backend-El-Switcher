import pytest
from app.db.db import GameStatus
from app.schemas.logs import LogMessageSchema
from app.services.logs import get_log_history
from app.services import game_events
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


@pytest.mark.asyncio
async def test_get_chat_history(test_client):
    db = TestingSessionLocal()
    reset_db()
    game = create_game(db, GameStatus.INGAME)

    await game_events.emit_log(1, "LOG HOLA", db)

    log_history = await get_log_history(game_id=game.id, db=db)

    assert log_history[0].message == "LOG HOLA"
    assert len(log_history) == 1
