import json
import pytest
from sqlalchemy.orm import Session
from unittest.mock import AsyncMock, patch
from sqlalchemy.exc import SQLAlchemyError
from app.services.board import revert_move_state
from app.db.db import ParallelBoard, SquarePiece, CardMove, Color
from app.errors.handlers import NotFoundError


@pytest.fixture
def db_session():
    # Setup a mock database session
    session = AsyncMock(spec=Session)
    return session


@pytest.mark.asyncio
async def test_revert_move_success(db_session):
    game_id = 1
    player_id = 1

    # Mock ParallelBoard query
    parallel_board = ParallelBoard(
        board_id=game_id,
        player_id=player_id,
        state_id=1,
        state_data=json.dumps([{"color": "RED", "row": 0, "column": 0}]),
        move_asociated=1,
    )
    db_session.query(
        ParallelBoard
    ).filter_by.return_value.order_by.return_value.first.return_value = (
        parallel_board
    )
    db_session.query(ParallelBoard).filter_by.return_value.all.return_value = [
        parallel_board
    ]

    # Mock SquarePiece query
    square_piece = SquarePiece(
        color=Color.RED, row=0, column=0, board_id=game_id
    )
    db_session.query(SquarePiece).filter.return_value.all.return_value = [
        square_piece
    ]

    # Mock CardMove query
    card_move = CardMove(
        id=1, owner_id=player_id, played=True, game_id=game_id
    )
    db_session.query(CardMove).filter.return_value.first.return_value = (
        card_move
    )

    with patch(
        "app.services.board.game_events.emit_board", new_callable=AsyncMock
    ) as mock_emit_board, patch(
        "app.services.board.game_events.emit_opponents_total_mov_cards",
        new_callable=AsyncMock,
    ) as mock_emit_opponents_total_mov_cards, patch(
        "app.services.board.game_events.emit_cards", new_callable=AsyncMock
    ) as mock_emit_cards, patch(
        "app.services.board.game_events.emit_found_figures",
        new_callable=AsyncMock,
    ) as mock_emit_found_figures:

        await revert_move_state(game_id, player_id, db_session)

        # Assertions
        db_session.query(ParallelBoard).filter_by.assert_called_with(
            board_id=game_id, state_id=1
        )
        assert card_move.played == False
        mock_emit_board.assert_awaited_once_with(game_id, db_session)
        mock_emit_opponents_total_mov_cards.assert_awaited_once_with(
            game_id, db_session
        )
        mock_emit_cards.assert_awaited_once_with(
            game_id, player_id, db_session
        )
        mock_emit_found_figures.assert_awaited_once_with(game_id, db_session)


@pytest.mark.asyncio
async def test_revert_move_no_board_state(db_session):
    game_id = 1
    player_id = 1

    # Mock ParallelBoard query to return None
    db_session.query(
        ParallelBoard
    ).filter_by.return_value.order_by.return_value.first.return_value = None

    with pytest.raises(RuntimeError, match="No board state to revert"):
        await revert_move_state(game_id, player_id, db_session)

    db_session.query(ParallelBoard).filter_by.assert_called_with(
        board_id=game_id
    )


@pytest.mark.asyncio
async def test_revert_move_sqlalchemy_error(db_session):
    game_id = 1
    player_id = 1

    # Mock ParallelBoard query to raise SQLAlchemyError
    db_session.query(
        ParallelBoard
    ).filter_by.return_value.order_by.return_value.first.side_effect = (
        SQLAlchemyError
    )

    with pytest.raises(RuntimeError, match="Error canceling move"):
        await revert_move_state(game_id, player_id, db_session)

    db_session.rollback.assert_called_once()
