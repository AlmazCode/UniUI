import sys
import pygame

from typing import NoReturn

from .math.vector2 import Vector2
from .tools.console import Console
from .utils import system
from .time import Time


class Screen:

    Time = Time()
    Instance = None
    
    def __init__(self, 
                 title: str = "UniUI Window",
                 referense_resolution: Vector2 = Vector2(1920, 1080),
                 resolution: Vector2 = Vector2(1920, 1080),
                 priority: float = 0.5,
                 refresh_rate: int = -1,
                 pg_flags: int = 0,
                 vsync: bool = True
    ):
        
        if Screen.Instance is None:
            Screen.Instance = self
        else:
            Console.error("Screen: the screen has already been created")
        
        self.title = title
        self.referense_resolution = referense_resolution
        self.resolution = None
        self.priority = priority
        self.pg_flags = pg_flags
        self.vsync = vsync
        self.scale_factor = None

        self._screen: pygame.Surface = None
        self.__system_refresh_rate = system.get_refresh_rate()
        self._refresh_rate_object = pygame.time.Clock()
        self._refresh_rate = (
            refresh_rate if isinstance(refresh_rate, int) and refresh_rate != -1 
                        else self.__system_refresh_rate
        )
        self._fps: int = None

        self.__initialize_screen(resolution)

    def __initialize_screen(self, resolution: Vector2) -> None:
        self._update_screen(resolution)
        pygame.display.set_caption(self.title)

        Console.clear()
        Console.log("The screen has been successfully initialized")
    
    def _update_screen(self, new_resolution: Vector2) -> None:
        if new_resolution.xy == (0, 0):
            info = pygame.display.Info()
            new_resolution.x = info.current_w
            new_resolution.y = info.current_h
        self._screen = pygame.display.set_mode(new_resolution.xy, self.pg_flags, vsync = self.vsync)
        self.resolution = new_resolution
        self._calc_scale_factor()
    
    def _calc_scale_factor(self) -> float:
        self.scale_factor = pow(self.resolution.x / self.referense_resolution.x, 1-self.priority) * \
                pow(self.resolution.y / self.referense_resolution.y, self.priority)

    def fps() -> int:
        return Screen.Instance._fps
    
    @staticmethod
    def quit() -> NoReturn:
        Console.log("The program has completed its work")
        pygame.quit()
        sys.exit(0)