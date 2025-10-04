import pygame

from .object import BaseObject
from .tools.console import Console
from .time import Time
from .screen import Screen

pygame.init()


class Scene:

    # Instance = None

    def __init__(self, name: str) -> None:

        self.name = name

        self._active = False

        self.__objects: list[BaseObject] = []
        self.__sorted_objects: dict[int, list[BaseObject]] = {}
        self.__deactivated_objects: dict[BaseObject, int] = {}
        self.__activated_objects: dict[BaseObject, int] = {}

        Screen.Instance.add_scene(self)

    
    def _add_object(self, object: BaseObject) -> None:
        if isinstance(object, BaseObject):
            self.__objects.append(object)
        else:
            Console.error("This object does not belong to the Object type")
    
    def _remove_object(self, object: BaseObject) -> None:
        if isinstance(object, BaseObject):
            self.__objects.remove(object)
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
        self.__sorted_objects.clear()

        for object in self.__objects:
            if object._layer not in self.__sorted_objects:
                self.__sorted_objects[object._layer] = [object]
            else:
                self.__sorted_objects[object._layer].append(object)
    
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
                object.draw(Screen.Instance._screen)
            
            # if settings.DEBUG_APP:
            #     Console.log(f"{len(self.__objects)} objects have been drawed\n{"-"*42}")
            
            pygame.display.update()