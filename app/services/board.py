from sqlalchemy.orm import Session
from app.schemas.board import PieceResponseSchema
from app.schemas.move import MakeMoveSchema
from app.db.db import Board, Color, SquarePiece, ParallelBoard, CardMove, Player
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

def make_move(move_data: MakeMoveSchema, db:Session):

    card_move = db.query(CardMove).filter(CardMove.id == move_data.movementCardId).first()
    if not card_move:
        raise ValueError("Invalid movementCardId")
    
    # Get the owner's player ID and the game ID
    player_id = card_move.owner_id
    player = db.query(Player).filter(Player.id == player_id).first()
    game_id = player.game_id
    
    # Save the current board state
    save_board(game_id, player_id, db)
    
    # Handle the piece switch logic
    switch_pieces(move_data.squarePieceId1, move_data.squarePieceId2, db)

    #emit board

    #?
    return 200

def save_board(game_id: int, player_id: int, db: Session):
    # Retrieve the current board state
    state_data = get_board(game_id, db)
    
    # Determine the state_id (1 to 3)
    existing_states = db.query(ParallelBoard).filter_by(board_id=game_id).order_by(ParallelBoard.state_id).all()
    if existing_states:
        latest_state_id = (existing_states[-1].state_id % 3) + 1
    else:
        latest_state_id = 1
    
    # Create and save the ParallelBoard object
    parallel_board = ParallelBoard(
        board_id=game_id,
        player_id=player_id,
        state_id=latest_state_id,
        state_data=state_data
    )
    db.add(parallel_board)
    db.commit()

def switch_pieces(piece_id1: int, piece_id2: int, db: Session):
    piece1 = db.query(SquarePiece).filter(SquarePiece.id == piece_id1).first()
    piece2 = db.query(SquarePiece).filter(SquarePiece.id == piece_id2).first()
    
    if piece1 and piece2:
        piece1.row, piece2.row = piece2.row, piece1.row
        piece1.column, piece2.column = piece2.column, piece1.column
        db.commit()