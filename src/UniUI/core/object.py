import pygame

from .math.vector2 import Vector2
from .tools.console import Console, CallerInfo
from .ui.align import Align
from .ui.transform import Transform

from typing import Union

def import_screen_module() -> None:
    global Screen
    from .screen import Screen

class BaseObject:
    def __init__(self, name: str, **args: dict[str, object]) -> None:
        # region vars
        self._name: str                     = name
        self._parent: BaseObject                = args.get("parent", None)
        self.__children: list[BaseObject]       = []
        self._root_caller_info: CallerInfo = Console._get_root_caller_info()

        self._active: bool                  = args.get("active", True)

        self._transform                     = Transform(
            args.get("position", Vector2(0, 0)),
            args.get("scale", Vector2(1, 1)),
            args.get("rotation", 0),
            args.get("width", 0),
            args.get("height", 0)
        )
        self._align: Align                  = args.get("align", Align.MIDDLE)
        # endregion

        # region method call
        if self._parent and isinstance(self._parent, BaseObject):
            self._parent.add_child(self)
        else:
            if Screen.Instance:
                Screen.Instance._add_object(self)
            else:
                raise Exception("Create a screen to create objects")
            
        self.__initialize_children(args.get("children", None))
        # endregion
    
    def __str__(self) -> str:
        return f"Object({self._name=}, {self._parent=})"

    def __initialize_children(self, children: list['BaseObject'] | None) -> None:
        if children is None:
            return
        
        for child in children:
            self.add_child(child)

    def add_child(self, child: 'BaseObject', update_parent: bool = True) -> None:
        if isinstance(child, BaseObject) and (child not in self.__children or not update_parent):
            if update_parent: child._parent = self
            self.__children.append(child)
        else:
            Console.error("add_child: child must be an Object")

    def remove_child(self, child: 'BaseObject', update_parent: bool = True) -> None:
        if isinstance(child, BaseObject):
            if update_parent: child._parent = None
            self.__children.remove(child)
        else:
            Console.error("remove_child: child must be an Object")
    
    # def _remove_children_from_screen(self) -> None:
    #     for child in self.__children:
    #         child._remove_children_from_screen()
    #         Screen.Instance._remove_object(child)
    
    # def _return_children_from_screen(self) -> None:
    #     for child in self.__children:
    #         child._return_children_from_screen()
    #         Screen.Instance._add_object(child)
    
    def _get_align_position(self) -> Vector2:
        start = Screen.Instance.transform
        end = Vector2(0, 0)

        match self._align:
            case Align.MIDDLE:
                end.x = start._width // 2 - self._transform._width // 2
                end.y = start._height // 2 - self._transform._height // 2
            case Align.LEFT:
                end.x = 0
                end.y = start._height // 2 - self._transform._height // 2
            case Align.RIGHT:
                end.x = start._width - self._transform._width
                end.y = start._height // 2 - self._transform._height // 2
            case Align.TOP:
                end.x = start._width // 2 - self._transform._width // 2
                end.y = 0
            case Align.BOTTOM:
                end.x = start._width // 2 - self._transform._width // 2
                end.y = start._height - self._transform._height

            case Align.TOPLEFT:
                end.x = 0
                end.y = 0
            case Align.TOPRIGHT:
                end.x = start._width - self._transform._width
                end.y = 0
            
            case Align.BOTTOMLEFT:
                end.x = 0
                end.y = start._height - self._transform._height
            case Align.BOTTOMRIGHT:
                end.x = start._width - self._transform._width
                end.y = start._height - self._transform._height
            
            case _:
                Console.error("Invalid align value", True, self.__root_caller_info)

        return end
    
    def get_root(self) -> 'BaseObject':
        obj = self
        while obj.parent is not None:
            obj = obj.parent
        return obj
    
    #region properties
    # @property
    # def position(self) -> Vector2:
    #     return self._position

    @property
    def transform(self) -> Transform:
        return self._transform
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def parent(self) -> 'BaseObject':
        return self._parent
    
    @property
    def active(self) -> bool:
        return self._active

    @property
    def align(self) -> Align:
        return self._align


    @property
    def global_position(self) -> Vector2:
        if self._parent:
            return self._transform.position + self._parent.global_position
        return self._transform.position

    @property
    def global_scale(self) -> Vector2:
        if self._parent:
            return self._transform.scale * self._parent.global_scale
        return self._transform.scale
    #endregion
    
    #region setters
    # @position.setter
    # def position(self, value: Vector2) -> None:
    #     if isinstance(value, Vector2):
    #         self._position = value
    #     else:
    #         Console.error("The value can only be a vector")
    
    @transform.setter
    def transform(self, value: Transform) -> None:
        if isinstance(value, Transform):
            self._transform = value
        else:
            Console.error(f"Expected value for 'transform', got {type(value).__name__}")
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            value = str(value)

        self._name = value
    
    @parent.setter
    def parent(self, value: Union['BaseObject', None]) -> None:
        if isinstance(value, BaseObject | None) and value not in self.__children:
            if value is not None:
                if self._parent is None:
                    Screen.Instance._remove_object(self)
                else:
                    self._parent.remove_child(self)
                self._parent = value
                self._parent.add_child(self)
            elif self._parent is not None:
                Screen.Instance._add_object(self)
                self._parent.remove_child(self)
        else:
            Console.error(f"Expected value for 'parent', got {type(value).__name__}")
    
    @active.setter
    def active(self, value: bool) -> None:
        if isinstance(value, bool):
            
            # activating object
            if value and not self._active:
                Screen.Instance._activate_object(self, 0 if self._parent is not None else 1)
            
            # deactivating object
            elif not value and self._active:
                if self._parent is None or (self.get_root().active and self._parent.active):
                    Screen.Instance._deactivate_object(self, 0 if self._parent is not None else 1)
            
            self._active = value
        else:
            Console.error(f"Expected bool for 'active', got {type(value).__name__}")

    @align.setter
    def align(self, value: Align) -> None:
        if isinstance(value, Align):
            self._align = value
        else:
            Console.error(f"Expected value for 'align', got {type(value).__name__}")
    #endregion

    def update(self) -> None:
        for child in self.__children:
            if child.active:
                child.update()

    def draw(self, surface: pygame.Surface) -> None:
        for child in self.__children:
            if child.active:
                child.draw(surface)