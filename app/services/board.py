from sqlalchemy.orm import Session
from app.schemas.board import PieceResponseSchema
from app.db.db import Board, Color, SquarePiece
from typing import List, Dict
import random

def create_board(game_id: int, db: Session) -> List[PieceResponseSchema]:
    board = Board(game_id=game_id)
    db.add(board)
    db.commit()
    db.refresh(board)


    #debe ser una lista con los colores posibles, siendo 9 de cada uno 
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
                board_id=board.game_id  
            )

            db.add(square_piece)
    db.commit()


def get_pieces(game_id: int, db: Session):
    return db.query(SquarePiece).filter(SquarePiece.board_id == game_id).all()

def get_board(game_id: int, db: Session) -> List[PieceResponseSchema]:
    square_pieces = get_pieces(game_id, db)
    return [PieceResponseSchema(
                squarePieceId=piece.id,
                color=piece.color.name,  # Enum to string
                row=piece.row,
                column=piece.column
            ).model_dump() for piece in square_pieces]