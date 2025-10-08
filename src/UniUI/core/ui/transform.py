import numbers

from ..math.vector2 import Vector2
from ..utils.event import Event
from ..tools.console import Console
from typing import Callable

class Transform:
    def __init__(self,
                 position: Vector2 = None,
                 scale: Vector2 = None,
                 rotation: Vector2 = None,
                 width: float = None,
                 height: float = None,
                 on_property_changed_callback: Callable[[], None] = None
    ) -> None:
        
        self._on_property_changed = Event([on_property_changed_callback] if on_property_changed_callback is not None else [])

        self._position  = position if position is not None and isinstance(position, Vector2) else Vector2(0, 0)
        self._scale     = Vector2(scale._x, scale._y, self._on_property_changed) \
            if scale is not None and isinstance(scale, Vector2) else Vector2(1, 1, self._on_property_changed)
        self._rotation  = rotation if rotation is not None and isinstance(rotation, numbers.Real) else 0
        self._width     = width if width is not None and isinstance(width, float | int) else 0
        self._height    = height if height is not None and isinstance(height, float | int) else 0
        self._size      = Vector2(self._width, self._height)
    
    @property
    def position(self) -> Vector2:
        return self._position

    @property
    def scale(self) -> Vector2:
        return self._scale
    
    @property
    def size(self) -> Vector2:
        return self._size

    @property
    def rotation(self) -> numbers.Real:
        return self._rotation

    @property
    def width(self) -> Vector2:
        return self._width
    
    @property
    def height(self) -> Vector2:
        return self._height

    @property
    def wh(self) -> tuple[float | int, float |int]:
        return self._width, self._height


    @position.setter
    def position(self, value: Vector2) -> None:
        if isinstance(value, Vector2):
            self._position = value
        else:
            Console.error("The value can only be a vector")
    
    @scale.setter
    def scale(self, value: Vector2) -> None:
        if isinstance(value, Vector2):
            self._scale = value
            self._on_property_changed.invoke()
        else:
            Console.error("The value can only be a vector")
    
    @rotation.setter
    def rotation(self, value: numbers.Real) -> None:
        if isinstance(value, numbers.Real):
            self._rotation = value
            self._on_property_changed.invoke()
        else:
            Console.error("The value can only be a vector")
    
    @width.setter
    def width(self, value: float | int) -> None:
        if isinstance(value, float | int):
            self._width = value
            self._size = Vector2(self._width, self._height)
            self._on_property_changed.invoke()
        else:
            Console.error("The value can only be a float or an integer")
    
    @height.setter
    def height(self, value: float | int) -> None:
        if isinstance(value, float | int):
            self._height = value
            self._size = Vector2(self._width, self._height)
            self._on_property_changed.invoke()
        else:
            Console.error("The value can only be a float or an integer")
    
    @wh.setter
    def wh(self, value: tuple[float | int, float |int]) -> None:
        if isinstance(value, tuple):
            if len(value) == 2:
                call_event: bool = False
                if isinstance(value[0], float | int):
                    self._width = value[0]
                    call_event = True
                else:
                    Console.error("The width can only be a float or an integer")
                
                if isinstance(value[1], float | int):
                    self._height = value[1]
                    call_event = True
                else:
                    Console.error("The height can only be a float or an integer")
                
                if call_event:
                    self._on_property_changed.invoke()
            else:
                Console.error("The size of the tuple should be 2")
        else:
            Console.error("The value can must be tuple of [float|int, float|int]")