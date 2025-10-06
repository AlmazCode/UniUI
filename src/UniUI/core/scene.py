import pygame

from .object import BaseObject
from .tools.console import Console
from .time import Time
from .screen import Screen

from collections import defaultdict
from typing import Callable

pygame.init()


class Scene:

    def __init__(self, name: str, init_func: Callable[['Scene'], None]) -> None:

        self.name = name

        self._active = False

        self.__objects: list[BaseObject] = []
        self.__sorted_objects: dict[int, list[BaseObject]] = {}
        self.__deactivated_objects: dict[BaseObject, int] = {}
        self.__activated_objects: dict[BaseObject, int] = {}
        self.__init_func = init_func
        self._is_loaded = False

    
    def _add_object(self, object: BaseObject) -> None:
        if isinstance(object, BaseObject):
            self.__objects.append(object)
            self._sort_objects()
        else:
            Console.error("This object does not belong to the Object type")
    
    def _remove_object(self, object: BaseObject) -> None:
        if isinstance(object, BaseObject):
            self.__objects.remove(object)
            self._sort_objects()
        else:
            Console.error("This object does not belong to the Object type")
        
    def _activate_object(self, object: BaseObject, mode: int) -> None:
        if isinstance(object, BaseObject):
            self.__activated_objects[object] = mode
            if self.__deactivated_objects.get(object, None):
                self.__deactivated_objects.pop(object)
        else:
            Console.error("This object does not belong to the Object type")
    
    def _deactivate_object(self, object: BaseObject, mode: int) -> None:
        if isinstance(object, BaseObject):
            self.__deactivated_objects[object] = mode
            if self.__activated_objects.get(object, None):
                self.__activated_objects.pop(object)
        else:
            Console.error("This object does not belong to the Object type")
    
    def _sort_objects(self) -> None:
        layers_dict = defaultdict(list)
        for obj in self.__objects:
            layers_dict[obj.layer].append(obj)

        self.__sorted_objects = dict(sorted(layers_dict.items()))
    
    def load(self):
        self.__init_func(self)
        self._is_loaded = True
        self.start()

    def unload(self):
        self._is_loaded = False
        
        for obj in self.__objects:
            obj.destroy()

        self.__objects.clear()
        self.__sorted_objects.clear()
        self.__activated_objects.clear()
        self.__deactivated_objects.clear()
    
    def start(self) -> None:

        self._active = True
        
        while self._active:
            Screen.Instance._screen.fill(0)
            Time._update_delta_time(Screen.Instance._refresh_rate_object.tick(Screen.Instance._refresh_rate) / 1000)
            Screen.Instance._fps = int(Screen.Instance._refresh_rate_object.get_fps())

            events: list[pygame.event.Event] = pygame.event.get()

            # events handle
            for event in events:
                if event.type == pygame.QUIT:
                    Screen.quit()
            
            # updating
            for layer in self.__sorted_objects:
                for obj in self.__sorted_objects[layer]:
                    obj.update()
            
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
            for layer in self.__sorted_objects:
                for obj in self.__sorted_objects[layer]:
                    obj.draw(Screen.Instance._screen)
            
            # if settings.DEBUG_APP:
            #     Console.log(f"{len(self.__objects)} objects have been drawed\n{"-"*42}")
            
            pygame.display.update()