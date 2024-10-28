import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.orm import Session

from app.services.game_list_events import emit_game_list
from app.db.db import Game, GameStatus


@pytest.fixture
def mock_db_session():
    db_session = MagicMock(spec=Session)
    return db_session


@pytest.fixture
def mock_sio():
    with patch(
        "app.services.game_list_events.sio.sio_game_list.emit",
        new_callable=AsyncMock,
    ) as mock_emit:
        yield mock_emit


@pytest.mark.asyncio
async def test_emit_game_list_no_games(mock_db_session, mock_sio):
    mock_db_session.query.return_value.filter.return_value.all.return_value = (
        []
    )

    await emit_game_list(mock_db_session)

    mock_sio.assert_called_once_with("game_list", [])


@pytest.mark.asyncio
async def test_emit_game_list_with_games(mock_db_session, mock_sio):
    mock_game = Game(
        id=1,
        name="Test Game",
        status=GameStatus.LOBBY,
        players=[],
        max_players=4,
    )
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        mock_game
    ]

    await emit_game_list(mock_db_session)

    expected_response = [
        {
            "gameId": mock_game.id,
            "gameName": mock_game.name,
            "connectedPlayers": len(mock_game.players),
            "maxPlayers": mock_game.max_players,
            "isPublic": True,
        }
    ]

    mock_sio.assert_called_once_with("game_list", expected_response)
