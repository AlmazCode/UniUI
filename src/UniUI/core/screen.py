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
        self.resolution = resolution
        self.pg_flags = pg_flags
        self.vsync = vsync

        self._screen: pygame.Surface = None
        self.__system_refresh_rate = system.get_refresh_rate()
        self._refresh_rate_object = pygame.time.Clock()
        self._refresh_rate = (
            refresh_rate if isinstance(refresh_rate, int) and refresh_rate != -1 
                        else self.__system_refresh_rate
        )
        self._fps: int = None

        self.__scenes: dict[str, 'Scene'] = {}
        self.__last_loaded_scene: 'Scene' = None

        self.__initialize_screen()

    def __initialize_screen(self) -> None:
        if self.resolution.xy == (0, 0):
            info = pygame.display.Info()
            self.resolution.x = info.current_w
            self.resolution.y = info.current_h
        self._screen = pygame.display.set_mode(self.resolution.xy, self.pg_flags, vsync = self.vsync)
        pygame.display.set_caption(self.title)

        # Console.clear()
        Console.log("The screen has been successfully initialized")

    @property
    def fps(self) -> int:
        return self._fps
    
    def add_scene(self, scene: 'Scene') -> None:
        if scene is not None and scene.name not in self.__scenes:
            self.__scenes[scene.name] = scene
    
    def load_scene(self, name: str) -> None:

        from .scene import Scene
        if isinstance(self.__last_loaded_scene, Scene):
            self.__last_loaded_scene._active = False

        if name in self.__scenes:
            self.__scenes[name].start()
    
    def load_scene(self, scene: 'Scene') -> None:

        from .scene import Scene
        if isinstance(self.__last_loaded_scene, Scene):
            self.__last_loaded_scene._active = False

        if scene.name in self.__scenes:
            self.__scenes[scene.name].start()
    
    def get_scene_by_name(self, name: str) -> 'Scene':
        if name in self.__scenes:
            return self.__scenes[name]
        return None
    
    @staticmethod
    def quit() -> NoReturn:
        Console.log("The program has completed its work")
        pygame.quit()
        sys.exit(0)