import random
import json
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.db import (
    Board,
    Color,
    SquarePiece,
    ParallelBoard,
    CardMove,
    Player,
    MoveType,
    GameStatus,
)
from app.errors.handlers import NotFoundError
from app.schemas.board import PieceResponseSchema, BlockColorSchema
from app.schemas.move import MakeMoveSchema
from app.services import game_events
from app.services.game_player_service import get_game, get_player


def create_board(game_id: int, db: Session) -> List[PieceResponseSchema]:
    board = Board(game_id=game_id)
    db.add(board)
    db.commit()
    db.refresh(board)

    # debe ser una lista con los colores posibles, siendo 9 de cada uno
    possible_colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW] * 9

    # 6x6 board
    for row in range(6):
        for column in range(6):
            # Elegir un color aleatorio para cada pieza
            random_color = random.choice(possible_colors)
            possible_colors.remove(random_color)

            # Crear una instancia de SquarePiece
            square_piece = SquarePiece(
                color=random_color,
                row=row,
                column=column,
                board_id=board.game_id,
            )

            db.add(square_piece)
    db.commit()


def get_pieces(game_id: int, db: Session):
    return db.query(SquarePiece).filter(SquarePiece.board_id == game_id).all()


def get_board(game_id: int, db: Session) -> List[PieceResponseSchema]:
    square_pieces = get_pieces(game_id, db)
    return [
        PieceResponseSchema(
            squarePieceId=piece.id,
            color=piece.color.name,  # Enum to string
            row=piece.row,
            column=piece.column,
        ).model_dump()
        for piece in square_pieces
    ]


def get_square_pieces(piece_id1: int, piece_id2: int, db: Session):
    """Valida y obtiene las fichas colores en base a su ID"""
    if not piece_id1 or not piece_id2:
        raise ValueError("Both piece IDs must be provided")
    if piece_id1 == piece_id2:
        raise ValueError("Pieces are the same")

    piece1 = db.query(SquarePiece).filter(SquarePiece.id == piece_id1).first()
    piece2 = db.query(SquarePiece).filter(SquarePiece.id == piece_id2).first()

    if not piece1 or not piece2:
        raise ValueError("One or both pieces not found")

    return piece1, piece2


async def make_move(
    game_id: int, player_id: int, move_data: MakeMoveSchema, db: Session
):
    """Realiza un movimiento en el tablero"""
    try:
        card_move = (
            db.query(CardMove)
            .filter(CardMove.id == move_data.movementCardId)
            .first()
        )
        if not card_move:
            raise ValueError("Invalid movementCardId")

        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise NotFoundError("Player not found")

        piece1, piece2 = get_square_pieces(
            move_data.squarePieceId1, move_data.squarePieceId2, db
        )

        if not validate_move(piece1, piece2, card_move.move):
            raise ValueError("Invalid move")

        state_id = save_board(game_id, player_id, card_move.id, db)
        switch_pieces(piece1, piece2, state_id, db)

        card_move.played = True
        db.commit()

        await game_events.emit_log(
            game_id,
            f"{player.name} ha jugado su movimiento {card_move.move.value[1]}.",
            db,
        )
        await game_events.emit_cards(game_id, player_id, db)
        await game_events.emit_board(game_id, db)
        await game_events.emit_found_figures(game_id, db)
        await game_events.emit_opponents_total_mov_cards(game_id, db)

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error making move: {e}")
    except ValueError as e:
        raise ValueError(f"{e}")


def save_board(game_id: int, player_id: int, movCard_id: int, db: Session):
    """Guarda el estado del tablero en la base de datos"""
    try:
        state_data = json.dumps(get_board(game_id, db))

        existing_states = (
            db.query(ParallelBoard)
            .filter_by(board_id=game_id)
            .order_by(ParallelBoard.state_id)
            .all()
        )
        if existing_states:
            latest_state_id = (existing_states[-1].state_id % 3) + 1
        else:
            latest_state_id = 1

        parallel_board = ParallelBoard(
            board_id=game_id,
            player_id=player_id,
            state_id=latest_state_id,
            state_data=state_data,
            move_asociated=movCard_id,
        )
        db.add(parallel_board)
        db.commit()
        return latest_state_id
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error saving board state: {e}")


def switch_pieces(piece1: int, piece2: int, state_id: int, db: Session):
    """Intercambia dos fichas de colores en el tablero"""
    try:
        piece1.row, piece2.row = piece2.row, piece1.row
        piece1.column, piece2.column = piece2.column, piece1.column
        piece1.partial_id = state_id
        piece2.partial_id = state_id
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error switching pieces: {e}")


def validate_move(
    piece1: SquarePiece, piece2: SquarePiece, move_type: MoveType
):
    row_diff = abs(piece1.row - piece2.row)
    col_diff = abs(piece1.column - piece2.column)

    row_rdiff = piece1.row - piece2.row
    col_rdiff = piece1.column - piece2.column

    if move_type == MoveType.MOV_1:  # CRUCE DIAGONAL CON UN ESPACIO
        return row_diff == 2 and col_diff == 2
    elif move_type == MoveType.MOV_2:  # CRUCE EN LINEA CON UN ESPACIOS
        return (row_diff == 2 and col_diff == 0) or (
            row_diff == 0 and col_diff == 2
        )
    elif move_type == MoveType.MOV_3:  # CRUCE EN LINEA CONTIGUO
        return (row_diff == 1 and col_diff == 0) or (
            row_diff == 0 and col_diff == 1
        )
    elif move_type == MoveType.MOV_4:  # CRUCE DIAGONAL CONTIGUO
        return row_diff == 1 and col_diff == 1
    elif (
        move_type == MoveType.MOV_5
    ):  # CRUCE EN L A LA IZQUIERDA CON DOS ESPACIOS)
        return (
            (row_rdiff == -2 and col_rdiff == 1)
            or (row_rdiff == 2 and col_rdiff == -1)
        ) or (
            (row_rdiff == 1 and col_rdiff == 2)
            or (row_rdiff == -1 and col_rdiff == -2)
        )
    elif (
        move_type == MoveType.MOV_6
    ):  # CRUCE EN L A LA DERECHA CON DOS ESPACIOS
        return (
            (row_rdiff == -2 and col_rdiff == -1)
            or (row_rdiff == 2 and col_rdiff == 1)
        ) or (
            (row_rdiff == 1 and col_rdiff == -2)
            or (row_rdiff == -1 and col_rdiff == 2)
        )
    elif move_type == MoveType.MOV_7:  # CRUCE EN LINEA AL LATERAL
        return (
            (
                (piece2.row == 0 or piece2.row == 5)
                and piece1.column == piece2.column
            )
            or (
                (piece2.column == 0 or piece2.column == 5)
                and piece1.row == piece2.row
            )
            or (
                (piece1.row == 0 or piece1.row == 5)
                and piece1.column == piece2.column
            )
            or (
                (piece1.column == 0 or piece1.column == 5)
                and piece1.row == piece2.row
            )
        )
    else:
        raise ValueError("Invalid move type")


async def validate_and_cancel_move(game_id: int, player_id: int, db: Session):
    """Valida y cancela el último movimiento jugado por un jugador"""
    player = get_player(player_id, db)
    game = get_game(game_id, db)

    if game.status != GameStatus.INGAME:
        raise ValueError("Game is not in progress")

    if player.turn != game.turn:
        raise ValueError("It's not your turn")

    player = get_player(player_id, db)
    await game_events.emit_log(
        game_id, f"{player.name} ha cancelado un movimiento.", db
    )
    await revert_move_state(game_id, player_id, db)


async def revert_move_state(game_id: int, player_id: int, db: Session):
    """Revierte el último movimiento jugado por un jugador"""
    try:
        parallel_board = (
            db.query(ParallelBoard)
            .filter_by(board_id=game_id)
            .order_by(ParallelBoard.state_id.desc())
            .first()
        )
        if not parallel_board:
            raise ValueError("No board state to revert")

        previous_states = (
            db.query(ParallelBoard)
            .filter_by(board_id=game_id, state_id=parallel_board.state_id)
            .all()
        )
        for state in previous_states:
            db.delete(state)
        db.commit()

        # Reemplazar el board por el parallel board
        square_pieces = get_pieces(game_id, db)
        for piece in square_pieces:
            db.delete(piece)
        db.commit()

        for piece in json.loads(parallel_board.state_data):
            square_piece = SquarePiece(
                color=Color[piece["color"]],
                row=piece["row"],
                column=piece["column"],
                board_id=game_id,
            )
            db.add(square_piece)

        # Devolverle la carta al jugador
        used_card = (
            db.query(CardMove)
            .filter(
                CardMove.id == parallel_board.move_asociated,
                CardMove.owner_id == player_id,
                CardMove.played == True,
                CardMove.game_id == game_id,
            )
            .first()
        )
        used_card.played = False
        db.commit()

        await game_events.emit_board(game_id, db)
        await game_events.emit_opponents_total_mov_cards(game_id, db)
        await game_events.emit_cards(game_id, player_id, db)
        await game_events.emit_found_figures(game_id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error canceling move: {e}")
    except ValueError as e:
        raise RuntimeError(f"Validation error: {e}")


# Delete all ParallelBoards and SquarePieces.partial_id
def delete_partial_cache(game_id: int, db: Session):
    """Elimina la cache parcial de un juego"""
    try:
        db.query(ParallelBoard).filter(
            ParallelBoard.board_id == game_id
        ).delete()
        db.query(SquarePiece).filter(SquarePiece.board_id == game_id).update(
            {SquarePiece.partial_id: None}
        )
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error deleting partial cache: {e}")


async def undo_played_moves(game_id: int, player_id: int, db: Session):
    """Deshace todos los movimientos jugados de un jugador en una partida"""
    try:
        played_card_moves = (
            db.query(CardMove)
            .filter(
                CardMove.owner_id == player_id,
                CardMove.played == True,
                CardMove.game_id == game_id,
            )
            .all()
        )

        if not played_card_moves:
            return

        for _ in played_card_moves:
            await revert_move_state(game_id, player_id, db)
        await game_events.emit_log(
            game_id, f"Los movimientos parciales se han revertido.", db
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error deleting partial cache: {e}")


async def set_block_color(game_id: int, color: Color, db: Session):
    """Establece el color prohibido en el tablero"""
    try:
        board = db.query(Board).filter(Board.game_id == game_id).first()
        board.block_color = color

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error setting block color: {e}")


def get_blocked_color(game_id: int, db: Session):
    """Obtiene el color bloqueado en el tablero"""
    board = db.query(Board).filter(Board.game_id == game_id).first()
    response = BlockColorSchema(
        blockedColor=board.block_color.name if board.block_color else None
    )

    return response.model_dump()
