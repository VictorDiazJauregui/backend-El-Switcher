import pytest
from unittest.mock import AsyncMock, patch

from app.db.db import GameStatus
from app.routers.sio_lobby import connect
from .db_setup import client, TestingSessionLocal, create_game, create_player


@pytest.fixture(scope="module")
def test_client():
    yield client


@pytest.mark.asyncio
@patch("app.routers.sio_lobby.parse_query_string")
@patch("app.routers.sio_lobby.Broadcast")
@patch("app.routers.sio_lobby.lobby_events.emit_players_lobby")
@patch("app.routers.sio_lobby.lobby_events.emit_can_start_game")
@patch("app.routers.sio_lobby.sio_lobby")
@patch("app.routers.sio_lobby.db_context")
async def test_connect_success(
    mock_db_context,
    mock_sio_lobby,
    mock_emit_can_start_game,
    mock_emit_players_lobby,
    mock_broadcast,
    mock_parse_query_string,
    test_client,
):

    # Create game and player in the database
    db = TestingSessionLocal()
    mock_db_context.return_value.__enter__.return_value = db
    game = create_game(db, GameStatus.LOBBY)
    player = create_player(db, game.id)

    mock_parse_query_string.return_value = (player.id, game.id)
    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    sid = "test_sid"
    environ = {}
    auth = {}

    await connect(sid, environ, auth)

    mock_parse_query_string.assert_called_once_with(environ)
    mock_broadcast.assert_called_once()
    mock_broadcast_instance.register_player_socket.assert_called_once_with(
        mock_sio_lobby, player.id, game.id, sid
    )
    mock_emit_players_lobby.assert_called_once_with(game.id, db)
    mock_emit_can_start_game.assert_called_once_with(game.id, db)


@pytest.mark.asyncio
@patch("app.routers.sio_lobby.parse_query_string")
@patch("app.routers.sio_lobby.Broadcast")
@patch("app.routers.sio_lobby.lobby_events.emit_players_lobby")
@patch("app.routers.sio_lobby.lobby_events.emit_can_start_game")
@patch("app.routers.sio_lobby.sio_lobby")
@patch("app.routers.sio_lobby.db_context")
async def test_connect_game_nonexistant(
    mock_db_context,
    mock_sio_lobby,
    mock_emit_can_start_game,
    mock_emit_players_lobby,
    mock_broadcast,
    mock_parse_query_string,
    test_client,
):

    # Create game and player in the database
    db = TestingSessionLocal()
    mock_db_context.return_value.__enter__.return_value = db
    game = create_game(db, GameStatus.LOBBY)
    player = create_player(db, game.id)

    mock_parse_query_string.return_value = (player.id, 999)
    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    sid = "test_sid"
    environ = {}
    auth = {}

    # Test when game does not exist
    await connect(sid, environ, auth)
    mock_emit_players_lobby.assert_not_called()
    mock_emit_can_start_game.assert_not_called()


@pytest.mark.asyncio
@patch("app.routers.sio_lobby.parse_query_string")
@patch("app.routers.sio_lobby.Broadcast")
@patch("app.routers.sio_lobby.lobby_events.emit_players_lobby")
@patch("app.routers.sio_lobby.lobby_events.emit_can_start_game")
@patch("app.routers.sio_lobby.sio_lobby")
@patch("app.routers.sio_lobby.db_context")
async def test_connect_player_error(
    mock_db_context,
    mock_sio_lobby,
    mock_emit_can_start_game,
    mock_emit_players_lobby,
    mock_broadcast,
    mock_parse_query_string,
    test_client,
):

    # Create game and player in the database
    db = TestingSessionLocal()
    mock_db_context.return_value.__enter__.return_value = db
    game = create_game(db, GameStatus.LOBBY)
    player = create_player(db, game.id)

    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    sid = "test_sid"
    environ = {}
    auth = {}

    # Test when player is not part of the game
    mock_parse_query_string.return_value = (999, game.id)
    await connect(sid, environ, auth)
    mock_emit_players_lobby.assert_not_called()
    mock_emit_can_start_game.assert_not_called()


@pytest.mark.asyncio
@patch("app.routers.sio_lobby.parse_query_string")
@patch("app.routers.sio_lobby.Broadcast")
@patch("app.routers.sio_lobby.lobby_events.emit_players_lobby")
@patch("app.routers.sio_lobby.lobby_events.emit_can_start_game")
@patch("app.routers.sio_lobby.sio_lobby")
@patch("app.routers.sio_lobby.db_context")
async def test_connect_not_lobby(
    mock_db_context,
    mock_sio_lobby,
    mock_emit_can_start_game,
    mock_emit_players_lobby,
    mock_broadcast,
    mock_parse_query_string,
    test_client,
):

    # Create game and player in the database
    db = TestingSessionLocal()
    mock_db_context.return_value.__enter__.return_value = db
    game = create_game(db, GameStatus.INGAME)
    player = create_player(db, game.id)

    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    sid = "test_sid"
    environ = {}
    auth = {}

    # Test when game is not in lobby status
    db.commit()
    db.refresh(game)
    mock_parse_query_string.return_value = (player.id, game.id)
    await connect(sid, environ, auth)
    mock_emit_players_lobby.assert_not_called()
    mock_emit_can_start_game.assert_not_called()
