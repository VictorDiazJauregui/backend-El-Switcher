import pytest
from unittest.mock import AsyncMock, patch

from app.routers.sio_game_list import connect


@pytest.mark.asyncio
async def test_connect():
    sid = "test_sid"
    environ = {}
    auth = {}

    # Mock the db_context and game_list_events
    with patch(
        "app.routers.sio_game_list.db_context"
    ) as mock_db_context, patch(
        "app.routers.sio_game_list.game_list_events.emit_game_list",
        new_callable=AsyncMock,
    ) as mock_emit_game_list:

        mock_db = mock_db_context.return_value.__enter__.return_value

        await connect(sid, environ, auth)

        mock_db_context.assert_called_once()
        mock_emit_game_list.assert_awaited_once_with(mock_db)
