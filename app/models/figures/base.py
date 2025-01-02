import numpy as np


class Figure:
    def __init__(self, type_name: str, matrix_figure: np.ndarray):
        self.matrix_figure = matrix_figure
        self.type_name = type_name

    def _to_binary(self, matrix: np.ndarray):
        """Convierte la matriz a una matriz binaria."""
        return np.where(matrix != None, 1, 0)

    def get_all_rotations(self):
        """Devuelve todas las rotaciones posibles de la figura (normal, 90°, 180°, 270°)."""
        rotations = [self.matrix_figure]  # Incluye la matriz original
        for k in range(1, 4):  # Rotar 90°, 180°, 270°
            rotated_matrix = np.rot90(self.matrix_figure, k=k)
            rotations.append(rotated_matrix)
        return rotations

    def matches_any_rotation(self, connected_component: np.ndarray):
        """Verifica si la matriz coincide con alguna rotación de la figura.
        Se abstrae del color de la componente conexa"""
        bin_connected_component = self._to_binary(connected_component)
        for rotation in self.get_all_rotations():
            if np.array_equal(
                self._to_binary(rotation), bin_connected_component
            ):
                return True
        return False
