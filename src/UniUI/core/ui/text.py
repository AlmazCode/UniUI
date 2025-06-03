import pygame
from ..object import Object
from ..math.vector2 import Vector2
from ..ui.color import Color
from ..ui.align import TextAlign
from ..tools.console import Console

DEFAULT_FONT = "Arial"

class Text(Object):
    def __init__(self, name: str, **args: dict[str, object]) -> None:
        super().__init__(name, **args)

        self._text: str = args.get("text", "Hello, World!")
        self._color: Color = args.get("color", Color())
        self._font_path: str | None = args.get("font", None)
        self._font_size: int = args.get("font_size", 16)
        self._text_align: TextAlign = args.get("text_align", TextAlign.LEFT)

        self.__font: pygame.font.Font = None
        self.__surface: pygame.Surface = None

        self._transform._on_property_changed.add_listener(self._on_transform_property_changed)

        self.__load_font()
        self.__update_surface()

    # === Properties ===
    @property
    def text(self) -> str:
        return self._text

    @property
    def color(self) -> Color:
        return self._color

    @property
    def font(self) -> str | None:
        return self._font_path

    @property
    def font_size(self) -> int:
        return self._font_size
    
    @property
    def text_align(self) -> str:
        return self._text_align
    
    # === Setters ===
    @text.setter
    def text(self, value: str) -> None:
        self._text = str(value)
        self.__update_surface()
    
    @color.setter
    def color(self, value: Color) -> None:
        if isinstance(value, Color):
            self._color = value
            self.__update_surface()
        else:
            Console.error("Invalid color value")
    
    @font.setter
    def font(self, value: str | None) -> None:
        if isinstance(value, (str, type(None))):
            self._font_path = value
            self.__load_font()
            self.__update_surface()
        else:
            Console.error("Font must be a path string or None")
    
    @font_size.setter
    def font_size(self, value: int) -> None:
        if isinstance(value, int):
            self._font_size = value
            self.__load_font()
            self.__update_surface()
        else:
            Console.error("Font size must be an integer")
    
    @text_align.setter
    def text_align(self, value: TextAlign) -> None:
        if isinstance(value, TextAlign):
            self._text_align = value
            self.__update_surface()
        else:
            Console.error("Text's Align must be an integer")

    # @Object.position.setter
    # def position(self, value: Vector2) -> Vector2:
    #     Object.position.fset(self, value)

    # @Object.scale.setter
    # def scale(self, value: Vector2) -> Vector2:
    #     Object.scale.fset(self, value)
    #     self.__update_surface()

    # === Private methods ===

    def __load_font(self) -> None:
        try:
            if self._font_path:
                self.__font = pygame.font.Font(self._font_path, self._font_size)
            else:
                self.__font = pygame.font.SysFont(DEFAULT_FONT, self._font_size)
        except Exception as e:
            Console.error(f"Failed to load font: {e}")
            self.__font = pygame.font.SysFont(DEFAULT_FONT, self._font_size)

    def __render_lines(self) -> tuple[dict[pygame.Surface, tuple[int, int]], int, int]:
        lines = self._text.split("\n")
        rendered_lines: dict[pygame.Surface, tuple[int, int]] = {}
        width = height = 0

        for line in lines:
            surf = self.__font.render(line, True, self._color.rgba)
            size = surf.get_size()
            rendered_lines[surf] = size
            height += size[1]
            width = max(width, size[0])

        return rendered_lines, width, height

    def __update_surface(self) -> None:
        rendered_lines, width, height = self.__render_lines()
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        x = y = 0
        for surf in rendered_lines:
            match self._text_align:
                case TextAlign.MIDDLE:
                    x = width // 2 - rendered_lines[surf][0] // 2
                case TextAlign.RIGHT:
                    x = width - rendered_lines[surf][0]
                case _:
                    x = 0

            surface.blit(surf, (x, y))
            y += rendered_lines[surf][1]

        pygame.draw.rect(surface, (255, 0, 0), surface.get_rect(), 1)  # Debug border

        # Apply scaling
        if self.global_scale.x != 1 and self.global_scale.y != 1:
            new_size = (Vector2(width, height) * self.global_scale).xy
            surface = pygame.transform.smoothscale(surface, new_size)
        
        self._transform._width = width
        self._transform._height = height
        self.__surface = surface
    
    def _on_transform_property_changed(self):
        self.__update_surface()
    
    # === Public Methods ===
    
    def get_render_position(self) -> Vector2:
        return self._get_align_position() + self.global_position

    # === Pygame Hooks ===

    def update(self) -> None:
        super().update()

    def draw(self, surface: pygame.Surface) -> None:
        if self.__surface:
            surface.blit(self.__surface, self.get_render_position().xy)
        super().draw(surface)