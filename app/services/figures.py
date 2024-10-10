from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from sqlalchemy import func, select

from app.schemas.game import GameCreateSchema, GameListSchema, ListSchema, StartResponseSchema
from app.schemas.player import PlayerResponseSchema
from app.schemas.board import PieceResponseSchema
from app.db.db import Game, Player, GameStatus, Turn, CardMove, CardFig, MoveType, FigureType, Board, SquarePiece, Color
import random
from app.services import lobby_events, game_events, game_list_events
from app.services.cards import assign_figure_cards
from app.models.figures import get_all_figures
from collections import defaultdict
import numpy as np



def get_matrix(game_id: int, db: Session) -> np.matrix:
    """
    Obtener la matriz de colores de un tablero.
    """
    board = db.query(Board).filter(Board.game_id == game_id).first()
    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Board for game {game_id} does not exist.")
    matrix = []
    for i in range(6):
        row = []
        for piece in board.square_pieces:
            if piece.row == i:
                row.append(piece.color)
        matrix.append(row)

    matrix = np.matrix(matrix)    
    return matrix


def filter_board_by_color(board: np.matrix, color: str) -> np.matrix:
    return np.where(board == color, board, None)



def depth_first_search(filtered_board: np.matrix, visited: np.matrix, row: int, col: int, color: Color):
    rows, cols = filtered_board.shape

    # Lista para almacenar las posiciones del componente conexo
    connected_component = []
    stack = [(row, col)]  # Pila de nodos por visitar

    min_row, max_row = row, row
    min_col, max_col = col, col

    while stack:
        row, col = stack.pop()

        if visited[row, col]:
            continue

        visited[row, col] = True

        # Agregar la posición a la componente
        connected_component.append((row, col))

        # Actualizamos los límites para definir el subarreglo
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

        # Revisar vecinos (arriba, abajo, izquierda, derecha)
        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + i, col + j

            if 0 <= new_row < rows and 0 <= new_col < cols:
                if filtered_board[new_row, new_col] == color and not visited[new_row, new_col]:
                    stack.append((new_row, new_col))

    # Crear un subarreglo del tamaño correcto
    subarray_rows = max_row - min_row + 1
    subarray_cols = max_col - min_col + 1
    subarray = np.full((subarray_rows, subarray_cols), None)

    # Poner los elementos de la componente en el subarreglo
    for r, c in connected_component:
        subarray[r - min_row, c - min_col] = (color, r, c)

    return subarray



def find_connected_components(filtered_board: np.matrix, color: str) -> list:
    rows, cols = filtered_board.shape

    visited = np.zeros((rows, cols), dtype=bool)  # Matriz de visitados
    components = []

    for row in range(rows):
        for col in range(cols):
            if filtered_board[row, col] is not None and not visited[row, col]:
                # Realiza DFS para obtener la componente conexa
                component = depth_first_search(filtered_board, visited, row, col, color)
                components.append(component)

    return components





def find_all_color_components(board: np.matrix) -> list:
    all_connected_components = []

    for color in [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]:
        filtered_board = filter_board_by_color(board, color)
        components = find_connected_components(filtered_board, color)
        all_connected_components.extend(components) # Agregar todas las componentes a una lista
    
    return all_connected_components



def extract_figures_from_board(board: np.matrix) -> dict:
    """Encuentra todas las figuras en el tablero y retorna un diccionario de figuras agrupadas por tipo."""
    all_connected_components = find_all_color_components(board)

    figures_by_type = defaultdict(list)

    for component in all_connected_components:
        for figure in get_all_figures():
            if figure.matches_any_rotation(component):
                figures_by_type[figure.type_name].append(component)

    return figures_by_type



def testing(game_id: int, db: Session) -> list:
    #test de funciones anteriormente nombradas
    matrix = get_matrix(game_id, db)
    figures_by_type = extract_figures_from_board(matrix)


    return figures_by_type