import numpy as np
from app.db.db import Color


class Figure:
    def __init__(self, type_name: str, matrix_figure: np.ndarray, figureCardId: int):
        self.matrix_figure = matrix_figure
        self.type_name = type_name
        self.figureCardId = figureCardId

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

            if np.array_equal(self._to_binary(rotation), bin_connected_component):
                return True
        return False

class fig1(Figure):
    def __init__(self):
        type_name = "fig1"
        matrix_figure = np.array(
            [
                ["*", "*", "*"],
                [None, "*", None],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure, 1)


class fig2(Figure):
    def __init__(self):
        type_name = "fig2"
        matrix_figure = np.array(
            [
                ["*", "*", None, None],
                [None, "*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 2)




class fig3(Figure):
    def __init__(self):
        type_name = "fig3"
        matrix_figure = np.array(
            [
                [None, None, "*", "*"],
                ["*", "*", "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure, 3)


class fig4(Figure):
    def __init__(self):
        type_name = "fig4"
        matrix_figure = np.array(
            [
                ["*", None, None],
                ["*", "*", None],
                [None, "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 4)


class fig5(Figure):
    def __init__(self):
        type_name = "fig5"
        matrix_figure = np.array(
            [
                ["*", "*", "*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 5)


class fig6(Figure):
    def __init__(self):
        type_name = "fig6"
        matrix_figure = np.array(
            [
                ["*", None, None],
                ["*", None, None],
                ["*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 6)


class fig7(Figure):
    def __init__(self):
        type_name = "fig7"
        matrix_figure = np.array(
            [
                ["*", "*", "*", "*"],
                [None, None, None, "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 7)


class fig8(Figure):
    def __init__(self):
        type_name = "fig8"
        matrix_figure = np.array(
            [
                [None, None, None, "*"],
                ["*", "*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 8)


class fig9(Figure):
    def __init__(self):
        type_name = "fig9"
        matrix_figure = np.array(
            [
                [None, None, "*"],
                ["*", "*", "*"],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure, 9)


class fig10(Figure):
    def __init__(self):
        type_name = "fig10"
        matrix_figure = np.array(
            [
                [None, None, "*"],
                ["*", "*", "*"],
                ["*", None, None],
            ]
        )
        super().__init__(type_name, matrix_figure, 10)

class fig11(Figure):
    def __init__(self):
        type_name = "fig11"
        matrix_figure = np.array(
            [
                ["*", None, None],
                ["*", "*", "*"],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure, 11)

class fig12(Figure):
    def __init__(self):
        type_name = "fig12"
        matrix_figure = np.array(
            [
                ["*", None, None],
                ["*", "*", "*"],
                [None, None, "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 12)

class fig13(Figure):
    def __init__(self):
        type_name = "fig13"
        matrix_figure = np.array(
            [
                ["*", "*", "*", "*"],
                [None, None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure, 13)



class fig14(Figure):
    def __init__(self):
        type_name = "fig14"
        matrix_figure = np.array(
            [
                [None, None, "*", None],
                ["*", "*", "*", "*"], 
            ]
        )
        super().__init__(type_name, matrix_figure, 14)



class fig15(Figure):
    def __init__(self):
        type_name = "fig15"
        matrix_figure = np.array(
            [
                [None, "*", "*"],
                ["*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 15)


class fig16(Figure):
    def __init__(self):
        type_name = "fig16"
        matrix_figure = np.array(
            [
                ["*", None, "*"],
                ["*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 16)


class fig17(Figure):
    def __init__(self):
        type_name = "fig17"
        matrix_figure = np.array(
            [
                [None, "*", None],
                ["*", "*", "*"],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure, 17)


class fig18(Figure):
    def __init__(self):
        type_name = "fig18"
        matrix_figure = np.array(
            [
                ["*", "*", "*"],
                [None, "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure, 18)


class fig19(Figure):
    def __init__(self):
        type_name = "fig19"
        matrix_figure = np.array(
            [
                ["*", "*", "*"],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure, 19)



def get_all_figures():
    return [fig1(), fig2(), fig3(), fig4(), fig5(), fig6(), fig7(), fig8(), fig9(), fig10(), fig11(), fig12(), fig13(), fig14(), fig15(), fig16(), fig17(), fig18(), fig19()]

def get_figure_by_id(figure_id: int):
    return next((figure for figure in get_all_figures() if figure.figureCardId == figure_id), None)