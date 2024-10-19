import pytest
from unittest.mock import AsyncMock, patch

from app.services.game_events import emit_winner

from .db_setup import client, TestingSessionLocal, create_player


@pytest.fixture(scope="module")
def test_client():
    yield client


@pytest.mark.asyncio
@patch("app.services.game_events.Broadcast")
async def test_emit_winner(mock_broadcast):
    db = TestingSessionLocal()
    player = create_player(db, 1)

    # Mock Broadcast
    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    # Act
    await emit_winner(1, player.id, db)

    # Assert
    mock_broadcast_instance.broadcast.assert_called_once
