from enum import Enum

class Align(Enum):
    
    MIDDLE          = 1
    LEFT            = 2
    RIGHT           = 3
    TOP             = 4
    BOTTOM          = 5

    TOPLEFT         = 6
    TOPRIGHT        = 7
    
    BOTTOMLEFT      = 8
    BOTTOMRIGHT     = 9

class TextAlignX:

    MIDDLE  = 1
    LEFT    = 2
    RIGHT   = 3

class TextAlignY:

    MIDDLE  = 1
    TOP     = 2
    BOTTOM  = 3

class TextAlign:
    def __init__(self, x: TextAlignX = TextAlignX.MIDDLE, y: TextAlignY = TextAlignY.MIDDLE) -> None:
        self.x = x
        self.y = y