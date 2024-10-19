import pytest
from unittest.mock import AsyncMock, patch

from app.db.db import GameStatus
from app.services.lobby_events import (
    emit_can_start_game,
    emit_players_lobby,
    emit_game_started,
)
from .db_setup import client, TestingSessionLocal, create_game, create_player


@pytest.fixture(scope="module")
def test_client():
    yield client


@pytest.mark.asyncio
@patch("app.services.lobby_events.Broadcast")
@patch("app.services.lobby_events.sio")
async def test_emit_game_started(mock_sio, mock_broadcast):

    # Create a mock instance of Broadcast
    mock_broadcast_instance = mock_broadcast.return_value
    mock_broadcast_instance.broadcast = AsyncMock()

    # Call the function
    await emit_game_started(1)

    # Assert that broadcast was called with the correct parameters
    mock_broadcast_instance.broadcast.assert_called_once_with(
        mock_sio.sio_lobby, 1, "game_started", {"gameStarted": True}
    )


@pytest.mark.asyncio
@patch("app.services.lobby_events.Broadcast")
@patch("app.services.lobby_events.sio")
async def test_emit_can_start_game(mock_sio, mock_broadcast):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY)
    player = create_player(db, game.id)
    create_player(db, game.id)

    # Create a mock instance of Broadcast
    mock_broadcast_instance = mock_broadcast.return_value
    mock_broadcast_instance.send_to_player = AsyncMock()

    # Call the function
    await emit_can_start_game(game.id, db)

    # Assert that send_to_player was called with the correct parameters
    mock_broadcast_instance.send_to_player.assert_called_once_with(
        mock_sio.sio_lobby, player.id, "start_game", {"canStart": True}
    )


@pytest.mark.asyncio
@patch("app.services.lobby_events.Broadcast")
@patch("app.services.lobby_events.sio")
async def test_emit_can_start_game_not_enough_players(
    mock_sio, mock_broadcast
):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY)
    create_player(db, game.id)

    # Create a mock instance of Broadcast
    mock_broadcast_instance = mock_broadcast.return_value
    mock_broadcast_instance.send_to_player = AsyncMock()

    # Call the function
    await emit_can_start_game(game.id, db)

    # Assert


@pytest.mark.asyncio
@patch("app.services.lobby_events.Broadcast")
@patch("app.services.lobby_events.sio")
async def test_emit_can_start_game_too_many_players(mock_sio, mock_broadcast):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY)
    player = create_player(db, game.id)
    create_player(db, game.id)
    create_player(db, game.id)
    create_player(db, game.id)
    create_player(db, game.id)

    # Create a mock instance of Broadcast
    mock_broadcast_instance = mock_broadcast.return_value
    mock_broadcast_instance.send_to_player = AsyncMock()

    # Call the function
    await emit_can_start_game(game.id, db)

    # Assert that send_to_player was called with the correct parameters
    mock_broadcast_instance.send_to_player.assert_called_once_with(
        mock_sio.sio_lobby, player.id, "start_game", {"canStart": False}
    )


@pytest.mark.asyncio
@patch("app.services.lobby_events.Broadcast")
@patch("app.services.lobby_events.sio")
async def test_emit_players_lobby(mock_sio, mock_broadcast):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY)
    player1 = create_player(db, game.id)
    player2 = create_player(db, game.id)

    # Create a mock instance of Broadcast
    mock_broadcast_instance = mock_broadcast.return_value
    mock_broadcast_instance.broadcast = AsyncMock()

    # Call the function
    await emit_players_lobby(game.id, db)

    # Assert that broadcast was called with the correct parameters
    expected_player_list = [
        {"playerId": player1.id, "playerName": player1.name},
        {"playerId": player2.id, "playerName": player2.name},
    ]
    mock_broadcast_instance.broadcast.assert_called_once_with(
        mock_sio.sio_lobby, game.id, "player_list", expected_player_list
    )


@pytest.mark.asyncio
@patch("app.services.lobby_events.Broadcast")
@patch("app.services.lobby_events.sio")
async def test_emit_players_lobby_no_players(mock_sio, mock_broadcast):
    db = TestingSessionLocal()
    game = create_game(db, GameStatus.LOBBY)

    # Create a mock instance of Broadcast
    mock_broadcast_instance = mock_broadcast.return_value
    mock_broadcast_instance.broadcast = AsyncMock()

    # Call the function
    await emit_players_lobby(game.id, db)

    # Assert that broadcast was called with an empty player list
    mock_broadcast_instance.broadcast.assert_called_once_with(
        mock_sio.sio_lobby, game.id, "player_list", []
    )
