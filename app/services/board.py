from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.board import PieceResponseSchema
from app.schemas.move import MakeMoveSchema
from app.db.db import Board, Color, SquarePiece, ParallelBoard, CardMove, Player
from app.services.game_events import emit_board
from typing import List
import random

def create_board(game_id: int, db: Session) -> List[PieceResponseSchema]:
    board = Board(game_id=game_id)
    db.add(board)
    db.commit()
    db.refresh(board)


    #debe ser una lista con los colores posibles, siendo 9 de cada uno 
    possible_colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW] * 9



    list_of_pieces = []
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
                board_id=board.game_id  
            )

            list_of_pieces.append(PieceResponseSchema(color=square_piece.color,
                                row=square_piece.row,
                                column=square_piece.column).model_dump())
            db.add(square_piece)
    db.commit()

    return list_of_pieces

def get_board_repository(game_id: int, db: Session): # capaz que a futuro hacemos lo de repositories?...
    return db.query(SquarePiece).filter(SquarePiece.board_id == game_id).all()

def get_board(game_id: int, db: Session) -> List[PieceResponseSchema]:
    square_pieces = get_board_repository(game_id, db)
    return [PieceResponseSchema(
                color=piece.color.name,  # Enum to string
                row=piece.row,
                column=piece.column
            ).model_dump() for piece in square_pieces]

def make_move(move_data: MakeMoveSchema, db: Session):
    try:
        card_move = db.query(CardMove).filter(CardMove.id == move_data.movementCardId).first()
        if not card_move:
            raise ValueError("Invalid movementCardId")
        
        player_id = card_move.owner_id
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise ValueError("Player not found")
        game_id = player.game_id
        
        save_board(game_id, player_id, db)
        switch_pieces(move_data.squarePieceId1, move_data.squarePieceId2, db)
        emit_board(game_id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error making move: {e}")
    except ValueError as e:
        raise RuntimeError(f"Validation error: {e}")

    return 200

def save_board(game_id: int, player_id: int, db: Session):
    try:
        state_data = get_board(game_id, db)
        
        existing_states = db.query(ParallelBoard).filter_by(board_id=game_id).order_by(ParallelBoard.state_id).all()
        if existing_states:
            latest_state_id = (existing_states[-1].state_id % 3) + 1
        else:
            latest_state_id = 1
        
        parallel_board = ParallelBoard(
            board_id=game_id,
            player_id=player_id,
            state_id=latest_state_id,
            state_data=state_data
        )
        db.add(parallel_board)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error saving board state: {e}")

def switch_pieces(piece_id1: int, piece_id2: int, db: Session):
    try:
        piece1 = db.query(SquarePiece).filter(SquarePiece.id == piece_id1).first()
        piece2 = db.query(SquarePiece).filter(SquarePiece.id == piece_id2).first()
        
        if not piece1:
            raise ValueError("Piece 1 not found")
        if not piece2:
            raise ValueError("Piece 2 not found")

        piece1.row, piece2.row = piece2.row, piece1.row
        piece1.column, piece2.column = piece2.column, piece1.column
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error switching pieces: {e}")
    except ValueError as e:
        raise RuntimeError(f"Validation error: {e}")