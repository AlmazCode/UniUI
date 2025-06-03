from enum import Enum

class Align(Enum):
    
    MIDDLE          = 1
    LEFT            = 2
    RIGHT           = 3
    TOP             = 4
    BOTTOM          = 5

    TOPLEFT         = 6
    TOPRIGHT        = 7
    
    BOTTOMLEFT      = 9
    BOTTOMRIGHT     = 10

class TextAlign(Enum):
    MIDDLE  = 1
    LEFT    = 2
    RIGHT   = 3