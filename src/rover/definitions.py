from enum import Enum, auto

class Motion(Enum):
    FORWARD = auto()
    STOP = auto()
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()
    BOTH = auto()

class CMD(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    STOP = auto()
    PLUS = auto()
    MINUS = auto()
    UP = auto()
    DOWN = auto()
