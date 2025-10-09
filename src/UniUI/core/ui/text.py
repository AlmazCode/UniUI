import pygame
import pygame.freetype
import numbers

from ..object import BaseObject
from ..math.vector2 import Vector2
from ..ui.color import Color
from ..ui.align import TextAlign, TextAlignX, TextAlignY
from ..tools.console import Console
from ..screen import Screen


pygame.freetype.init()


DEFAULT_FONT_NAME = "Arial"
DEFAULT_FONT = pygame.freetype.SysFont(DEFAULT_FONT_NAME, 0)
DEFAULT_FONT_SIZE = 16
DEFAULT_PADDING = 0


class Text(BaseObject):

    def __init__(self, name: str, scene: str, **args: dict[str, object]) -> None:
        super().__init__(name, scene, **args)

        self._text: str = args.get("text", "Hello, World!")
        self._color: Color = args.get("color", Color())
        self._font_size: float = args.get("font_size", DEFAULT_FONT_SIZE)
        self._text_align: TextAlign = args.get("text_align", TextAlign())
        
        padding = args.get("padding", None)
        self._padding: float = padding if isinstance(padding, numbers.Real) else DEFAULT_PADDING

        self._preffered_size: Vector2 = Vector2(0, 0)

        font = args.get("font", None)
        self.__font: pygame.freetype.Font = font if isinstance(font, pygame.freetype.Font) else DEFAULT_FONT
        self.__surface: pygame.Surface = None

        self.__update_surface()

    # === Properties ===
    @property
    def text(self) -> str:
        return self._text

    @property
    def color(self) -> Color:
        return self._color

    @property
    def font(self) -> pygame.freetype.Font:
        return self.__font

    @property
    def font_size(self) -> float:
        return self._font_size
    
    @property
    def text_align(self) -> str:
        return self._text_align

    @property
    def padding(self) -> str:
        return self._padding
    
    @property
    def preffered_size(self) -> Vector2:
        return self._preffered_size
    
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
        if isinstance(value, pygame.freetype.Font):
            self.__font = value
            self.__update_surface()
        else:
            Console.error("The font must be an object of type pygame.freetype.Font")
    
    @font_size.setter
    def font_size(self, value: numbers.Real) -> None:
        if isinstance(value, numbers.Real):
            self._font_size = value
            self.__update_surface()
        else:
            Console.error("The value must be an integer")
    
    @text_align.setter
    def text_align(self, value: TextAlign) -> None:
        if isinstance(value, TextAlign):
            self._text_align = value
            self.__update_surface()
        else:
            Console.error("The value must be an integer")
    
    @padding.setter
    def padding(self, value: numbers.Real) -> None:
        if isinstance(value, numbers.Real):
            self._padding = value
            self.__update_surface()
        else:
            Console.error("The value must be a number")
    
    @preffered_size.setter
    def preffered_size(self, value: Vector2) -> None:
        Console.error("You cannot change preffered_size, it is a private variable.")

    # === Private methods ===

    def __render_lines(self) -> tuple[dict[pygame.Surface, pygame.Rect], int, int]:
        lines = self._text.split("\n")
        lenght = len(lines)
        rendered_lines: dict[pygame.Surface, pygame.Rect] = {}
        width = height = 0

        for line in lines:
            surf, size = self.__font.render(
                text=line,
                fgcolor=self._color.rgba,
                size=self._font_size*Screen.Instance.scale_factor
            )

            surf = surf.convert_alpha()
            rendered_lines[surf] = size
            height += size.height
            width = max(width, size.width)

        height += self._padding * Screen.Instance.scale_factor * (lenght - 1)

        return rendered_lines, width, height

    def __update_surface(self) -> None:
        global_scale = self.global_scale
        rendered_lines, width, height = self.__render_lines()
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        y = 0
        for surf in rendered_lines:
            surf_size = rendered_lines[surf]
            if self._text_align.x == TextAlignX.RIGHT:
                x = width - surf_size.width
            elif self._text_align.x == TextAlignX.MIDDLE:
                x = (width - surf_size.width) // 2
            else:
                x = 0

            surface.blit(surf, (x, y))
            y += surf_size.height + self._padding * Screen.Instance.scale_factor

        # Apply rotation
        global_rotation = self.global_rotation
        if global_rotation != 0:
            surface = pygame.transform.rotozoom(surface, global_rotation, 1)
            width, height = surface.get_size()

        # Apply scaling
        if global_scale.x != 1 or global_scale.y != 1:
            new_size = (Vector2(width, height) * global_scale).xy
            surface = pygame.transform.smoothscale(surface, (max(0, new_size[0]), max(0, new_size[1])))
            width, height = surface.get_size()

        pygame.draw.rect(surface, (255, 0, 0), surface.get_rect(), 1)  # Debug border
        pygame.draw.line(surface, (255, 0, 0), (0, height // 2), (width, height // 2))
        pygame.draw.line(surface, (255, 0, 0), (width // 2, 0), (width // 2, height))

        self._preffered_size = Vector2(width, height)
        self.__surface = surface
    
    def _refurbish_interior(self):
        self.__update_surface()
        super()._refurbish_interior()
    
    def _get_text_align_offset(self, pos: Vector2) -> Vector2:
        """
        Calculates the offset for text alignment.
        """
        
        match self._text_align.x:
            case TextAlignX.RIGHT:
                pos.x += self._transform._width * Screen.Instance.scale_factor - self._preffered_size.x
            case TextAlignX.LEFT:
                ...
            case TextAlignX.MIDDLE:
                pos.x += self._transform._width * Screen.Instance.scale_factor // 2 - self._preffered_size.x // 2
        
        match self._text_align.y:
            case TextAlignY.BOTTOM:
                pos.y += self._transform._height * Screen.Instance.scale_factor - self._preffered_size.y
            case TextAlignY.TOP:
                ...
            case TextAlignY.MIDDLE:
                pos.y += self._transform._height * Screen.Instance.scale_factor // 2 - self._preffered_size.y // 2

        return pos

    # === Public Methods ===
    
    def get_render_position(self) -> Vector2:
        return self._get_text_align_offset(self.global_position)

    # === Pygame Hooks ===

    def update(self) -> None:
        super().update()

    def draw(self, surface: pygame.Surface) -> None:
        if self.__surface:
            
            # Позиция и размер контейнера (объекта)
            container_pos = self.global_position
            container_width = self._transform._width
            container_height = self._transform._height
            
            # Позиция текста (с учетом text_align внутри контейнера)
            render_pos = self.get_render_position()
            
            # Рисуем текст
            surface.blit(self.__surface, render_pos.xy)
            
            # Debug: белый прямоугольник - это контейнер объекта
            pygame.draw.rect(
                surface, 
                (255, 255, 255), 
                (*container_pos.xy, container_width*Screen.Instance.scale_factor, container_height*Screen.Instance.scale_factor), 
                1
            )
        
        super().draw(surface)