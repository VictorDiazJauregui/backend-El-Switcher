import numpy as np
from .base import Figure


class fig19(Figure):
    def __init__(self):
        super().__init__(
            "Figura Fácil 4",
            np.array(
                [
                    ["*", "*", "*"],
                    [None, "*", None],
                ]
            ),
        )


class fig20(Figure):
    def __init__(self):
        super().__init__(
            "Figura Fácil 1",
            np.array(
                [
                    [None, "*", "*"],
                    ["*", "*", None],
                ]
            ),
        )


class fig21(Figure):
    def __init__(self):
        super().__init__(
            "Figura Fácil 2",
            np.array(
                [
                    ["*", "*"],
                    ["*", "*"],
                ]
            ),
        )


class fig22(Figure):
    def __init__(self):
        super().__init__(
            "Figura Fácil 3",
            np.array(
                [
                    ["*", "*", None],
                    [None, "*", "*"],
                ]
            ),
        )


class fig23(Figure):
    def __init__(self):
        super().__init__(
            "Figura Fácil 5",
            np.array(
                [
                    ["*", "*", "*"],
                    [None, None, "*"],
                ]
            ),
        )


class fig24(Figure):
    def __init__(self):
        super().__init__(
            "Figura Fácil 6",
            np.array(
                [
                    ["*", "*", "*", "*"],
                ]
            ),
        )


class fig25(Figure):
    def __init__(self):
        super().__init__(
            "Figura Fácil 7",
            np.array(
                [
                    [None, None, "*"],
                    ["*", "*", "*"],
                ]
            ),
        )
