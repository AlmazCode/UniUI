from ..tools.console import Console

class Color:
    def __init__(self, r: int = 255, g: int = 255, b: int = 255, a: int = 255) -> None:
        self._r = self._clamp(r)
        self._g = self._clamp(g)
        self._b = self._clamp(b)
        self._a = self._clamp(a)

    def _clamp(self, value: int) -> int:
        if not isinstance(value, int):
            Console.warning(f"Invalid type for color value: {value}, expected int.")
            return 255
        return max(0, min(255, value))

    @property
    def r(self) -> int: return self._r
    @property
    def g(self) -> int: return self._g
    @property
    def b(self) -> int: return self._b
    @property
    def a(self) -> int: return self._a
    @property
    def rgba(self) -> tuple[int, int, int, int]: return (self._r, self._g, self._b, self._a)

    @r.setter
    def r(self, _): Console.warning("You cannot change the `R` channel individually")
    @g.setter
    def g(self, _): Console.warning("You cannot change the `G` channel individually")
    @b.setter
    def b(self, _): Console.warning("You cannot change the `B` channel individually")
    @a.setter
    def a(self, _): Console.warning("You cannot change the `A` channel individually")

    def __eq__(self, other) -> bool:
        return isinstance(other, Color) and self.rgba == other.rgba

    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"