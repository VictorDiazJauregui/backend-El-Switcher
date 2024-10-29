import pytest
from unittest.mock import AsyncMock, patch

from app.services.game_events import emit_timer, emit_winner

from .db_setup import client, TestingSessionLocal, create_player


@pytest.fixture(scope="module")
def test_client():
    yield client


@pytest.mark.asyncio
@patch("app.services.game_events.Broadcast")
@patch("app.services.game_events.end_turn")
@patch("app.services.game_events.asyncio.sleep")
@pytest.mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call' was never awaited:RuntimeWarning")
async def test_emit_timer(mock_sleep, mock_end_turn, mock_broadcast):
    db = TestingSessionLocal()
    player = create_player(db, 1)

    # Mock Broadcast
    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    # Act
    await emit_timer(1, player.id, db)

    # Assert
    assert mock_broadcast_instance.broadcast.call_count == 120
    mock_end_turn.assert_called_once_with(1, player.id, db)

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
