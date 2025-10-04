import numbers
import math

from ..tools.console import Console

class Vector2:

    def __init__(self, x: numbers.Real, y: numbers.Real) -> None:
        self._x = x if isinstance(x, numbers.Real) else 0.0
        self._y = y if isinstance(y, numbers.Real) else 0.0

    def __add__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, numbers.Real):
            return Vector2(self.x + other, self.y + other)
        Console.error("The value can only be a vector")

    def __sub__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, numbers.Real):
            return Vector2(self.x - other, self.y - other)
        Console.error("The value can only be a vector")

    def __mul__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, numbers.Real):
            return Vector2(self.x * other, self.y * other)
        Console.error("The value can only be a vector")

    def __truediv__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(
                self.x / other.x if other.x != 0 else float('inf'),
                self.y / other.y if other.y != 0 else float('inf')
            )
        elif isinstance(other, numbers.Real):
            return Vector2(
                self.x / other if other != 0 else float('inf'),
                self.y / other if other != 0 else float('inf')
            )
        Console.error("The value can only be a vector")

    def __eq__(self, other) -> bool:
        return isinstance(other, Vector2) and self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: numbers.Real) -> None:
        if isinstance(value, numbers.Real):
            self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: numbers.Real) -> None:
        if isinstance(value, numbers.Real):
            self._y = value

    @property
    def xy(self) -> tuple[float, float]:
        return (self._x, self._y)

    def magnitude(self) -> float:
        return math.hypot(self.x, self.y)

    def normalize(self) -> 'Vector2':
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return self / mag

zero_vector = Vector2(0, 0)
unit_vector = Vector2(1, 1)