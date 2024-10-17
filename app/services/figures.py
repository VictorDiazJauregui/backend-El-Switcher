import numpy as np
from collections import defaultdict

from sqlalchemy.orm import Session

from app.db.db import Board, Color
from app.errors.handlers import NotFoundError
from app.models.figures import get_all_figures

def get_matrix(game_id: int, db: Session) -> np.ndarray:
    """
    Obtener la matriz de colores de un tablero.
    """
    board = db.query(Board).filter(Board.game_id == game_id).first()
    if board is None:
        raise NotFoundError(f"Board for game {game_id} does not exist.")
    matrix = np.ndarray((6, 6), dtype=Color)
    for i in range(6):
        row = np.ndarray(6, dtype=Color)
        for piece in board.square_pieces:
            if piece.row == i:
                row[piece.column] = piece.color
        matrix[i] = row

       
    return matrix


def filter_board_by_color(board: np.ndarray, color: Color) -> np.matrix:
    return np.where(board == color, board, None)



def depth_first_search(filtered_board: np.ndarray, visited: np.ndarray, row: int, col: int, color: Color):
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



def find_connected_components(filtered_board: np.ndarray, color: str) -> list:
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





def find_all_color_components(board: np.ndarray) -> list:
    all_connected_components = []

    for color in [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]:
        filtered_board = filter_board_by_color(board, color)
        components = find_connected_components(filtered_board, color)
        all_connected_components.extend(components) # Agregar todas las componentes a una lista
    
    return all_connected_components



def extract_figures_from_board(board: np.ndarray) -> dict:
    """Encuentra todas las figuras en el tablero y retorna un diccionario de figuras agrupadas por tipo."""
    all_connected_components = find_all_color_components(board)


    figures_by_type = defaultdict(list)

    for component in all_connected_components:
        for figure in get_all_figures():
            if figure.matches_any_rotation(component):
                figures_by_type[figure.type_name].append(component)
            
            

    return figures_by_type



def convert_to_serializable(figures_by_type: defaultdict) -> dict:
    """Convierte el defaultdict a un formato serializable."""
    serializable_dict = {}

    for figure_type, components in figures_by_type.items():
        serializable_components = []
        
        for component in components:
            # Convertir cada subarray en una estructura serializable
            serializable_component = []
            for row in component:
                serializable_row = []
                for cell in row:
                    if cell is None:
                        serializable_row.append(None)
                    else:
                        color, r, c = cell
                        # Convertimos el color a su representación de cadena
                        serializable_row.append({
                            "color": color.name,  # Convertir el objeto Color a una cadena
                            "row": r,
                            "col": c
                        })
                serializable_component.append(serializable_row)
            
            serializable_components.append(serializable_component)
        
        serializable_dict[figure_type] = serializable_components
    
    return serializable_dict



def figures_event(game_id: int, db: Session) -> list:
    #test de funciones anteriormente nombradas
    matrix = get_matrix(game_id, db)
    figures = extract_figures_from_board(matrix)
    figures = convert_to_serializable(figures)

    
    return figures