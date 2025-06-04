import pygame
import sys

pygame.init()

from typing import NoReturn

from .object import Object
from .math.vector2 import Vector2
from .tools.console import Console
from .utils.system import get_refresh_rate
from .time import Time
from .ui.transform import Transform
from . import settings

class Screen:

    Instance = None

    def __init__(self,
                 resolution: Vector2 = Vector2(480, 480), title: str = "UniUI Window", refresh_rate: int = -1,
                 flags: int = 0) -> None:

        if Screen.Instance is None:
            Screen.Instance = self
        else:
            Console.error("Screen: the screen has already been created")

        self.__system_refresh_rate = get_refresh_rate()
        self.title: str = title
        self.transform: Transform = Transform(
            None,
            None,
            None,
            resolution.x if isinstance(resolution, Vector2) else 0,
            resolution.y if isinstance(resolution, Vector2) else 0
        )
        self.flags: int = flags
        self.__screen: pygame.Surface = None
        self.__refresh_rate_object = pygame.time.Clock()
        self.__refresh_rate = (
            refresh_rate if isinstance(refresh_rate, int) and refresh_rate != -1 
                        else self.__system_refresh_rate
        )
        self.__fps = None
        self.__objects: list[Object] = []
        self.__deactivated_objects: dict[Object, int] = {}
        self.__activated_objects: dict[Object, int] = {}
        self.__initialize()
    
    @property
    def fps(self) -> float:
        return self.__fps
    
    def __initialize(self) -> None:
        if self.transform.wh == (0, 0):
            info = pygame.display.Info()
            self.transform.wh = (info.current_w, info.current_h)
        self.__screen = pygame.display.set_mode(self.transform.wh, self.flags, vsync=1)
        pygame.display.set_caption(self.title)

        Console.clear()
        Console.log("The screen has been successfully initialized")
    
    def _add_object(self, object: Object) -> None:
        if isinstance(object, Object):
            self.__objects.append(object)
        else:
            Console.error("This object does not belong to the Object type")
    
    def _remove_object(self, object: Object) -> None:
        if isinstance(object, Object):
            self.__objects.remove(object)
        else:
            Console.error("This object does not belong to the Object type")
        
    def _activate_object(self, object: Object, mode: int) -> None:
        if isinstance(object, Object):
            self.__activated_objects[object] = mode
            if self.__deactivated_objects.get(object, None):
                self.__deactivated_objects.pop(object)
        else:
            Console.error("This object does not belong to the Object type")
    
    def _deactivate_object(self, object: Object, mode: int) -> None:
        if isinstance(object, Object):
            self.__deactivated_objects[object] = mode
            if self.__activated_objects.get(object, None):
                self.__activated_objects.pop(object)
        else:
            Console.error("This object does not belong to the Object type")
    
    def quit(self) -> NoReturn:
        Console.log("The program has completed its work")
        pygame.quit()
        sys.exit(0)
    
    def start(self) -> None:
        
        while 1:
            self.__screen.fill(0)
            Time._update_delta_time(self.__refresh_rate_object.tick(self.__refresh_rate) / 1000)
            self.__fps = int(self.__refresh_rate_object.get_fps())

            events: list[pygame.event.Event] = pygame.event.get()

            # events handle
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()
            
            # updating
            for object in self.__objects:
                object.update()
            
            # if settings.DEBUG_APP:
            #     Console.log(f"{len(self.__objects)} objects have been updated")
            
            # activating objects
            if self.__activated_objects:
                while len(self.__activated_objects) > 0:
                    (object, mode) = self.__activated_objects.popitem()
                    if mode == 1:
                        self._add_object(object)
                    else:
                        object._parent.add_child(object, False)
            
            # deactivating objects
            if self.__deactivated_objects:
                while len(self.__deactivated_objects) > 0:
                    (object, mode) = self.__deactivated_objects.popitem()
                    if mode == 1:
                        self._remove_object(object)
                    else:
                        object._parent.remove_child(object, False)
            
            # drawing
            for object in self.__objects:
                object.draw(self.__screen)
            
            # if settings.DEBUG_APP:
            #     Console.log(f"{len(self.__objects)} objects have been drawed\n{"-"*42}")
            
            pygame.display.update()