import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.orm import Session

from app.db.db import Player, CardMove
from app.schemas.player import PlayerResponseSchema
from app.services.game_events import (
    emit_players_game,
    emit_opponents_total_mov_cards,
)
from app.routers import sio_game as sio


@pytest.fixture
def mock_db_session():
    # Create a mock database session
    session = AsyncMock(spec=Session)
    players = [
        Player(
            id=1,
            name="Player1",
            game_id=1,
            card_moves=[
                CardMove(id=1, played=False),
                CardMove(id=2, played=True),
            ],
        ),
        Player(
            id=2,
            name="Player2",
            game_id=1,
            card_moves=[
                CardMove(id=3, played=False),
                CardMove(id=4, played=False),
            ],
        ),
    ]
    session.query(Player).filter.return_value.all.return_value = players
    return session


@pytest.fixture
def mock_broadcast():
    # Create a mock Broadcast class
    with patch("app.services.game_events.Broadcast") as MockBroadcast:
        mock_broadcast_instance = MockBroadcast.return_value
        mock_broadcast_instance.broadcast = AsyncMock()
        mock_broadcast_instance.get_sid = AsyncMock()
        mock_broadcast_instance.send_to_player = AsyncMock()
        yield mock_broadcast_instance


@pytest.mark.asyncio
async def test_emit_players_game(mock_db_session, mock_broadcast):
    game_id = 1

    await emit_players_game(game_id, mock_db_session)

    # Verify that the broadcast method was called with the correct arguments
    expected_player_list = [
        PlayerResponseSchema(playerId=1, playerName="Player1").model_dump(),
        PlayerResponseSchema(playerId=2, playerName="Player2").model_dump(),
    ]
    mock_broadcast.broadcast.assert_called_once_with(
        sio.sio_game, game_id, "player_list", expected_player_list
    )


@pytest.mark.asyncio
async def test_emit_opponents_total_mov_cards(mock_db_session, mock_broadcast):
    game_id = 1

    await emit_opponents_total_mov_cards(game_id, mock_db_session)

    # Verify that the broadcast method was called with the correct arguments
    expected_result = [
        {"playerId": 1, "totalMovCards": 1},
        {"playerId": 2, "totalMovCards": 2},
    ]
    mock_broadcast.broadcast.assert_called_once_with(
        sio.sio_game, game_id, "opponents_total_mov_cards", expected_result
    )
