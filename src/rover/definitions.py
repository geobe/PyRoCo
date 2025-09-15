from enum import Enum, auto

class Motion(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    STOP = auto()
    LEFT = auto()
    RIGHT = auto()
    BOTH = auto()
    PLUS = auto()
    MINUS = auto()
    UP = auto()
    DOWN = auto()
    DIRECTION = auto()
    SPEED = auto()
    NONE = auto()

# class CMD(Enum):
    # FORWARD = auto()
    # BACKWARD = auto()
    # STOP = auto()
