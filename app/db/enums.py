import enum


class GameStatus(enum.Enum):
    LOBBY = "Lobby"
    INGAME = "Ingame"
    FINISHED = "Finished"


class Turn(enum.Enum):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class FigureType(enum.Enum):
    # Easy figures
    EASY_1 = (1, "Figura Fácil 1")
    EASY_2 = (2, "Figura Fácil 2")
    EASY_3 = (3, "Figura Fácil 3")
    EASY_4 = (4, "Figura Fácil 4")
    EASY_5 = (5, "Figura Fácil 5")
    EASY_6 = (6, "Figura Fácil 6")
    EASY_7 = (7, "Figura Fácil 7")
    # Hard figures
    HARD_1 = (1, "Figura Difícil 1")
    HARD_2 = (2, "Figura Difícil 2")
    HARD_3 = (3, "Figura Difícil 3")
    HARD_4 = (4, "Figura Difícil 4")
    HARD_5 = (5, "Figura Difícil 5")
    HARD_6 = (6, "Figura Difícil 6")
    HARD_7 = (7, "Figura Difícil 7")
    HARD_8 = (8, "Figura Difícil 8")
    HARD_9 = (9, "Figura Difícil 9")
    HARD_10 = (10, "Figura Difícil 10")
    HARD_11 = (11, "Figura Difícil 11")
    HARD_12 = (12, "Figura Difícil 12")
    HARD_13 = (13, "Figura Difícil 13")
    HARD_14 = (14, "Figura Difícil 14")
    HARD_15 = (15, "Figura Difícil 15")
    HARD_16 = (16, "Figura Difícil 16")
    HARD_17 = (17, "Figura Difícil 17")
    HARD_18 = (18, "Figura Difícil 18")


class MoveType(enum.Enum):
    MOV_1 = (1, "CRUCE DIAGONAL CON UN ESPACIO")
    MOV_2 = (2, "CRUCE EN LINEA CON UN ESPACIO")
    MOV_3 = (3, "CRUCE EN LINEA CONTIGUO")
    MOV_4 = (4, "CRUCE DIAGONAL CONTIGUO")
    MOV_5 = (5, "CRUCE EN L A LA IZQUIERDA CON DOS ESPACIOS")
    MOV_6 = (6, "CRUCE EN L A LA DERECHA CON DOS ESPACIOS")
    MOV_7 = (7, "CRUCE EN LINEA AL LATERAL")


class Color(enum.Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    YELLOW = "Yellow"
