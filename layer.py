from enum import IntEnum, auto

class Layer(IntEnum):
    BACKGROUND = auto()
    OBSTACLE = auto()
    PIPE = auto()
    FLOOR = auto()
    PLAYER = auto()
    SCORE = auto()
    OVERLAY = auto()
    UI = auto()