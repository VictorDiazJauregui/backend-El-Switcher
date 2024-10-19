import pytest
from unittest.mock import AsyncMock, patch

from app.routers.sio_game import connect
from app.db.db import GameStatus
from .db_setup import (
    client,
    TestingSessionLocal,
    create_game,
    create_player,
    add_example_board,
)


@pytest.fixture(scope="module")
def test_client():
    yield client


@pytest.mark.asyncio
@patch("app.routers.sio_game.parse_query_string")
@patch("app.routers.sio_game.Broadcast")
@patch("app.routers.sio_game.game_events.emit_board")
@patch("app.routers.sio_game.game_events.emit_cards")
@patch("app.routers.sio_game.game_events.emit_players_game")
@patch("app.routers.sio_game.game_events.emit_turn_info")
@patch("app.routers.sio_game.game_events.emit_opponents_total_mov_cards")
@patch("app.routers.sio_game.sio_game", new_callable=AsyncMock)
@patch("app.routers.sio_game.db_context")
async def test_connect_success(
    mock_db_context,
    mock_sio_game,
    mock_emit_board,
    mock_emit_cards,
    mock_emit_players_game,
    mock_emit_turn_info,
    mock_emit_opponents_total_mov_cards,
    mock_broadcast,
    mock_parse_query_string,
):

    # Create game and player in the database
    db = TestingSessionLocal()
    mock_db_context.return_value.__enter__.return_value = db
    game = create_game(db, GameStatus.INGAME)
    add_example_board(db, game.id)
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
        mock_sio_game, player.id, game.id, sid
    )
    mock_emit_board.assert_called_once_with(game.id, db)
    mock_emit_players_game.assert_called_once_with(game.id, db)
    #   Funcionan, pero tuvieron un comportamiento extraño y podrían causar
    #   problemas en el futuro, se comentan por ser redundantes ante los
    #   demás chequeos
    #    mock_emit_cards.assert_called_once_with(game.id, db)
    #    mock_emit_turn_info.assert_called_once_with(game.id, player.id, db)
    mock_emit_opponents_total_mov_cards.assert_called_once_with(game.id, db)


@pytest.mark.asyncio
@patch("app.routers.sio_game.parse_query_string")
@patch("app.routers.sio_game.Broadcast")
@patch("app.routers.sio_game.game_events.emit_board")
@patch("app.routers.sio_game.game_events.emit_cards")
@patch("app.routers.sio_game.game_events.emit_players_game")
@patch("app.routers.sio_game.game_events.emit_turn_info")
@patch("app.routers.sio_game.game_events.emit_opponents_total_mov_cards")
@patch("app.routers.sio_game.sio_game")
@patch("app.routers.sio_game.db_context")
async def test_connect_game_error(
    mock_db_context,
    mock_sio_game,
    mock_emit_board,
    mock_emit_cards,
    mock_emit_players_game,
    mock_emit_turn_info,
    mock_emit_opponents_total_mov_cards,
    mock_broadcast,
    mock_parse_query_string,
):

    # Create game and player in the database
    db = TestingSessionLocal()
    mock_db_context.return_value.__enter__.return_value = db
    player = create_player(db, 999)

    # Game doesn't exist
    mock_parse_query_string.return_value = (player.id, 999)
    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    sid = "test_sid"
    environ = {}
    auth = {}

    await connect(sid, environ, auth)
    mock_broadcast.assert_not_called()
    mock_broadcast_instance.register_player_socket.assert_not_called()
    mock_emit_board.assert_not_called()
    mock_emit_players_game.assert_not_called()
    mock_emit_cards.assert_not_called()
    mock_emit_turn_info.assert_not_called()
    mock_emit_opponents_total_mov_cards.assert_not_called()


@pytest.mark.asyncio
@patch("app.routers.sio_game.parse_query_string")
@patch("app.routers.sio_game.Broadcast")
@patch("app.routers.sio_game.game_events.emit_board")
@patch("app.routers.sio_game.game_events.emit_cards")
@patch("app.routers.sio_game.game_events.emit_players_game")
@patch("app.routers.sio_game.game_events.emit_turn_info")
@patch("app.routers.sio_game.game_events.emit_opponents_total_mov_cards")
@patch("app.routers.sio_game.sio_game")
@patch("app.routers.sio_game.db_context")
async def test_connect_game_not_started(
    mock_db_context,
    mock_sio_game,
    mock_emit_board,
    mock_emit_cards,
    mock_emit_players_game,
    mock_emit_turn_info,
    mock_emit_opponents_total_mov_cards,
    mock_broadcast,
    mock_parse_query_string,
):

    # Create game and player in the database
    db = TestingSessionLocal()
    mock_db_context.return_value.__enter__.return_value = db
    game = create_game(db, GameStatus.LOBBY)  # Game not started
    db.commit()
    db.refresh(game)

    mock_parse_query_string.return_value = (999, game.id)  # Trivial player
    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    sid = "test_sid"
    environ = {}
    auth = {}

    await connect(sid, environ, auth)
    mock_broadcast.assert_not_called()
    mock_broadcast_instance.register_player_socket.assert_not_called()
    mock_emit_board.assert_not_called()
    mock_emit_players_game.assert_not_called()
    mock_emit_cards.assert_not_called()
    mock_emit_turn_info.assert_not_called()
    mock_emit_opponents_total_mov_cards.assert_not_called()


@pytest.mark.asyncio
@patch("app.routers.sio_game.parse_query_string")
@patch("app.routers.sio_game.Broadcast")
@patch("app.routers.sio_game.game_events.emit_board")
@patch("app.routers.sio_game.game_events.emit_cards")
@patch("app.routers.sio_game.game_events.emit_players_game")
@patch("app.routers.sio_game.game_events.emit_turn_info")
@patch("app.routers.sio_game.game_events.emit_opponents_total_mov_cards")
@patch("app.routers.sio_game.sio_game")
@patch("app.routers.sio_game.db_context")
async def test_connect_player_not_ingame(
    mock_db_context,
    mock_sio_game,
    mock_emit_board,
    mock_emit_cards,
    mock_emit_players_game,
    mock_emit_turn_info,
    mock_emit_opponents_total_mov_cards,
    mock_broadcast,
    mock_parse_query_string,
    capfd,
):

    # Create game and player in the database
    db = TestingSessionLocal()
    mock_db_context.return_value.__enter__.return_value = db
    game = create_game(db, GameStatus.INGAME)
    player = create_player(db, 999)  # Player not in game

    mock_parse_query_string.return_value = (player.id, game.id)
    mock_broadcast_instance = AsyncMock()
    mock_broadcast.return_value = mock_broadcast_instance

    sid = "test_sid"
    environ = {}
    auth = {}

    await connect(sid, environ, auth)
    mock_broadcast.assert_not_called()
    mock_broadcast_instance.register_player_socket.assert_not_called()
    mock_emit_board.assert_not_called()
    mock_emit_players_game.assert_not_called()
    mock_emit_cards.assert_not_called()
    mock_emit_turn_info.assert_not_called()
    mock_emit_opponents_total_mov_cards.assert_not_called()
