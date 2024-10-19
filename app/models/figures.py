import numpy as np
from app.db.db import Color
from sqlalchemy.orm import Session
from app.db.db import CardFig


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


class fig1(Figure):
    def __init__(self):
        type_name = "Figura Difícil 1"
        matrix_figure = np.array(
            [
                ["*", "*", "*"],
                [None, "*", None],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig2(Figure):
    def __init__(self):
        type_name = "Figura Difícil 2"
        matrix_figure = np.array(
            [
                ["*", "*", None, None],
                [None, "*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig3(Figure):
    def __init__(self):
        type_name = "Figura Difícil 3"
        matrix_figure = np.array(
            [
                [None, None, "*", "*"],
                ["*", "*", "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig4(Figure):
    def __init__(self):
        type_name = "Figura Difícil 4"
        matrix_figure = np.array(
            [
                ["*", None, None],
                ["*", "*", None],
                [None, "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig5(Figure):
    def __init__(self):
        type_name = "Figura Difícil 5"
        matrix_figure = np.array(
            [
                ["*", "*", "*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig6(Figure):
    def __init__(self):
        type_name = "Figura Difícil 6"
        matrix_figure = np.array(
            [
                ["*", None, None],
                ["*", None, None],
                ["*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig7(Figure):
    def __init__(self):
        type_name = "Figura Difícil 7"
        matrix_figure = np.array(
            [
                ["*", "*", "*", "*"],
                [None, None, None, "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig8(Figure):
    def __init__(self):
        type_name = "Figura Difícil 8"
        matrix_figure = np.array(
            [
                [None, None, None, "*"],
                ["*", "*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig9(Figure):
    def __init__(self):
        type_name = "Figura Difícil 9"
        matrix_figure = np.array(
            [
                [None, None, "*"],
                ["*", "*", "*"],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig10(Figure):
    def __init__(self):
        type_name = "Figura Difícil 10"
        matrix_figure = np.array(
            [
                [None, None, "*"],
                ["*", "*", "*"],
                ["*", None, None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig11(Figure):
    def __init__(self):
        type_name = "Figura Difícil 11"
        matrix_figure = np.array(
            [
                ["*", None, None],
                ["*", "*", "*"],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig12(Figure):
    def __init__(self):
        type_name = "Figura Difícil 12"
        matrix_figure = np.array(
            [
                ["*", None, None],
                ["*", "*", "*"],
                [None, None, "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig13(Figure):
    def __init__(self):
        type_name = "Figura Difícil 13"
        matrix_figure = np.array(
            [
                ["*", "*", "*", "*"],
                [None, None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig14(Figure):
    def __init__(self):
        type_name = "Figura Difícil 14"
        matrix_figure = np.array(
            [
                [None, None, "*", None],
                ["*", "*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig15(Figure):
    def __init__(self):
        type_name = "Figura Difícil 15"
        matrix_figure = np.array(
            [
                [None, "*", "*"],
                ["*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig16(Figure):
    def __init__(self):
        type_name = "Figura Difícil 16"
        matrix_figure = np.array(
            [
                ["*", None, "*"],
                ["*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig17(Figure):
    def __init__(self):
        type_name = "Figura Difícil 17"
        matrix_figure = np.array(
            [
                [None, "*", None],
                ["*", "*", "*"],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig18(Figure):
    def __init__(self):
        type_name = "Figura Difícil 18"
        matrix_figure = np.array(
            [
                ["*", "*", "*"],
                [None, "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig20(Figure):
    def __init__(self):
        type_name = "Figura Fácil 1"
        matrix_figure = np.array(
            [
                [None, "*", "*"],
                ["*", "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig21(Figure):
    def __init__(self):
        type_name = "Figura Fácil 2"
        matrix_figure = np.array(
            [
                ["*", "*"],
                ["*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig22(Figure):
    def __init__(self):
        type_name = "Figura Fácil 3"
        matrix_figure = np.array(
            [
                ["*", "*", None],
                [None, "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig19(Figure):
    def __init__(self):
        type_name = "Figura Fácil 4"
        matrix_figure = np.array(
            [
                ["*", "*", "*"],
                [None, "*", None],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig23(Figure):
    def __init__(self):
        type_name = "Figura Fácil 5"
        matrix_figure = np.array(
            [
                ["*", "*", "*"],
                [None, None, "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig24(Figure):
    def __init__(self):
        type_name = "Figura Fácil 6"
        matrix_figure = np.array(
            [
                ["*", "*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


class fig25(Figure):
    def __init__(self):
        type_name = "Figura Fácil 7"
        matrix_figure = np.array(
            [
                [None, None, "*"],
                ["*", "*", "*"],
            ]
        )
        super().__init__(type_name, matrix_figure)


def get_all_figures():
    return [
        fig1(),
        fig2(),
        fig3(),
        fig4(),
        fig5(),
        fig6(),
        fig7(),
        fig8(),
        fig9(),
        fig10(),
        fig11(),
        fig12(),
        fig13(),
        fig14(),
        fig15(),
        fig16(),
        fig17(),
        fig18(),
        fig19(),
        fig20(),
        fig21(),
        fig22(),
        fig23(),
        fig24(),
        fig25(),
    ]


def get_figure_by_id(figure_id: int, db: Session):
    return db.query(CardFig).filter(CardFig.id == figure_id).first()


def get_figure_type_by_id(figure_id: int, db: Session):
    return db.query(CardFig).filter(CardFig.id == figure_id).first().figure


def select_figure_by_his_type(type_name: str):
    if type_name == "Figura Difícil 1":
        return fig1()
    if type_name == "Figura Difícil 2":
        return fig2()
    if type_name == "Figura Difícil 3":
        return fig3()
    if type_name == "Figura Difícil 4":
        return fig4()
    if type_name == "Figura Difícil 5":
        return fig5()
    if type_name == "Figura Difícil 6":
        return fig6()
    if type_name == "Figura Difícil 7":
        return fig7()
    if type_name == "Figura Difícil 8":
        return fig8()
    if type_name == "Figura Difícil 9":
        return fig9()
    if type_name == "Figura Difícil 10":
        return fig10()
    if type_name == "Figura Difícil 11":
        return fig11()
    if type_name == "Figura Difícil 12":
        return fig12()
    if type_name == "Figura Difícil 13":
        return fig13()
    if type_name == "Figura Difícil 14":
        return fig14()
    if type_name == "Figura Difícil 15":
        return fig15()
    if type_name == "Figura Difícil 16":
        return fig16()
    if type_name == "Figura Difícil 17":
        return fig17()
    if type_name == "Figura Difícil 18":
        return fig18()
    if type_name == "Figura Fácil 4":
        return fig19()
    if type_name == "Figura Fácil 1":
        return fig20()
    if type_name == "Figura Fácil 2":
        return fig21()
    if type_name == "Figura Fácil 3":
        return fig22()
    if type_name == "Figura Fácil 5":
        return fig23()
    if type_name == "Figura Fácil 6":
        return fig24()
    if type_name == "Figura Fácil 7":
        return fig25()
    return None
