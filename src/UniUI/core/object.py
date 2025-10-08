import pygame

from .math.vector2 import Vector2, zero_vector, unit_vector
from .tools.console import Console, CallerInfo
from .ui.align import Align
from .ui.transform import Transform
from .screen import Screen

from typing import Union
from collections import defaultdict

DEFAULT_SIZE = Vector2(100, 100)

class BaseObject:
    
    def __init__(self, name: str, scene: 'Scene', **kwargs: dict[str, object]) -> None:

        # ======
        self._name: str                     = name
        self._scene: str                    = scene
        self._parent: BaseObject            = kwargs.get("parent", None)
        self.__children: list[BaseObject]   = []
        self.__sorted_children: dict[int, list[BaseObject]] = {}
        self._root_caller_info: CallerInfo  = Console._get_root_caller_info()

        self._active: bool                  = kwargs.get("active", True)

        self._transform                     = Transform(
            kwargs.get("position", zero_vector),
            kwargs.get("scale", unit_vector),
            kwargs.get("rotation", 0),
            kwargs.get("width", DEFAULT_SIZE.x),
            kwargs.get("height", DEFAULT_SIZE.y),
            self._on_transform_property_changed
        )
        self._align: Align                  = kwargs.get("align", Align.MIDDLE)
        self._layer: int                    = kwargs.get("layer", 0)
        # ======

        self.__scene = scene

        if self._parent and isinstance(self._parent, BaseObject):
            self._parent.add_child(self)
        else:
            if self.__scene:
                self.__scene._add_object(self)
            else:
                raise Exception("Create a scene to create objects")
            
        self.__initialize_children(kwargs.get("children", None))
    
    def __str__(self) -> str:
        return f"Object({self._name=}, {self._parent=})"

    def __initialize_children(self, children: list['BaseObject'] | None) -> None:
        if children is None:
            return
        
        for child in children:
            self.add_child(child, resort_objects=False)
        
        self._sort_children()
    
    def _get_align_offset_root(self, container_size: Vector2) -> Vector2:
        """
        Calculates the offset for the root object (without parent).
        Alignment relative to the container (usually the screen).
        """
        offset = Vector2(0, 0)
        
        match self._align:
            case Align.MIDDLE:
                offset.x = container_size.x // 2 - self._transform._width // 2
                offset.y = container_size.y // 2 - self._transform._height // 2
            case Align.LEFT:
                offset.x = 0
                offset.y = container_size.y // 2 - self._transform._height // 2
            case Align.RIGHT:
                offset.x = container_size.x - self._transform._width
                offset.y = container_size.y // 2 - self._transform._height // 2
            case Align.TOP:
                offset.x = container_size.x // 2 - self._transform._width // 2
                offset.y = 0
            case Align.BOTTOM:
                offset.x = container_size.x // 2 - self._transform._width // 2
                offset.y = container_size.y - self._transform._height
            case Align.TOPLEFT:
                offset.x = 0
                offset.y = 0
            case Align.TOPRIGHT:
                offset.x = container_size.x - self._transform._width
                offset.y = 0
            case Align.BOTTOMLEFT:
                offset.x = 0
                offset.y = container_size.y - self._transform._height
            case Align.BOTTOMRIGHT:
                offset.x = container_size.x - self._transform._width
                offset.y = container_size.y - self._transform._height
            case _:
                Console.error("Invalid align value", True, self._root_caller_info)
        
        return offset
    
    def _get_align_offset_child(self, parent_size: Vector2) -> Vector2:
        """
        Calculates the offset for a child object relative to its parent.
        Takes into account that the object is aligned OUTSIDE the parent in some cases.
        """
        offset = Vector2(0, 0)
        
        match self._align:
            case Align.MIDDLE:
                offset.x = parent_size.x // 2 - self._transform._width // 2
                offset.y = parent_size.y // 2 - self._transform._height // 2
            case Align.LEFT:
                offset.x = -self._transform._width
                offset.y = parent_size.y // 2 - self._transform._height // 2
            case Align.RIGHT:
                offset.x = parent_size.x
                offset.y = parent_size.y // 2 - self._transform._height // 2
            case Align.TOP:
                offset.x = parent_size.x // 2 - self._transform._width // 2
                offset.y = -self._transform._height
            case Align.BOTTOM:
                offset.x = parent_size.x // 2 - self._transform._width // 2
                offset.y = parent_size.y
            case Align.TOPLEFT:
                offset.x = -self._transform._width
                offset.y = -self._transform._height
            case Align.TOPRIGHT:
                offset.x = parent_size.x
                offset.y = -self._transform._height
            case Align.BOTTOMLEFT:
                offset.x = -self._transform._width
                offset.y = parent_size.y
            case Align.BOTTOMRIGHT:
                offset.x = parent_size.x
                offset.y = parent_size.y
            case _:
                Console.error("Invalid align value", True, self._root_caller_info)
        
        return offset

    def _get_align_offset(self) -> Vector2:
        """
        Calculates the offset for aligning an object.
        Uses different logic for root and child objects.
        """
        if self._parent is None:
            # Root object: alignment relative to the screen
            container_size = Vector2(*Screen.Instance.resolution.xy)
            return self._get_align_offset_root(container_size)
        else:
            # Child object: alignment relative to parent
            parent_size = self._parent._transform.size
            return self._get_align_offset_child(parent_size)

    def _sort_children(self) -> None:
        layers_dict = defaultdict(list)
        for obj in self.__children:
            layers_dict[obj.layer].append(obj)

        self.__sorted_children = dict(sorted(layers_dict.items()))
    
    def _on_transform_property_changed(self):
        for child in self.__children:
            child._on_transform_property_changed()
    
    #region properties
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
    def layer(self) -> int:
        return self._layer

    @property
    def global_position(self) -> Vector2:
        """
        Returns the global position of the object, taking into account:
        1. The position of the parent (if any)
        2. Alignment relative to the parent
        3. The local position of the object
        """
        align_offset = self._get_align_offset()
        
        if self._parent:
            # Global position = parent position + alignment offset + local position
            return self._parent.global_position + align_offset + self._transform.position
        else:
            # Root object: alignment offset + local position
            return align_offset + self._transform.position

    @property
    def global_scale(self) -> Vector2:
        if self._parent:
            return self._transform._scale * self._parent.global_scale
        return self._transform._scale
    
    @property
    def global_rotation(self) -> Vector2:
        if self._parent:
            return self._transform._rotation + self._parent.global_rotation
        return self._transform._rotation
    #endregion
    
    #region Setters
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
                    self.__scene._remove_object(self)
                else:
                    self._parent.remove_child(self)
                self._parent = value
                self._parent.add_child(self)
            elif self._parent is not None:
                self.__scene._add_object(self)
                self._parent.remove_child(self)
        else:
            Console.error(f"Expected value for 'parent', got {type(value).__name__}")
    
    @active.setter
    def active(self, value: bool) -> None:
        if isinstance(value, bool):
            
            # activating object
            if value and not self._active:
                # activation: 0 = child, 1 = root
                self.__scene._activate_object(self, 0 if self._parent is not None else 1)
            
            # deactivating object
            elif not value and self._active:
                if self._parent is None or (self.get_root().active and self._parent.active):
                    # activation: 0 = child, 1 = root
                    self.__scene._deactivate_object(self, 0 if self._parent is not None else 1)
            
            self._active = value
        else:
            Console.error(f"Expected bool for 'active', got {type(value).__name__}")

    @align.setter
    def align(self, value: Align) -> None:
        if isinstance(value, Align):
            self._align = value
        else:
            Console.error(f"Expected value for 'align', got {type(value).__name__}")
    
    @layer.setter
    def layer(self, value: int) -> None:
        if isinstance(value, int):
            if value != self._layer:
                self._layer = value
                if self._parent is not None:
                    self._parent._sort_children()
                else:
                    self.__scene._sort_objects()
        else:
            Console.error(f"Expected value for 'layer', got {type(value).__name__}")
    #endregion

    def destroy(self) -> None:
        for obj in self.__children:
            obj.destroy()

        del self.__children
        del self.__sorted_children
        del self

    def get_root(self) -> 'BaseObject':
        obj = self
        while obj.parent is not None:
            obj = obj.parent
        return obj

    def add_child(self, child: 'BaseObject', update_parent: bool = True, resort_objects: bool = True) -> None:
        if isinstance(child, BaseObject) and (child not in self.__children or not update_parent):
            if update_parent: child._parent = self
            self.__children.append(child)
            if resort_objects:
                self._sort_children()
        else:
            Console.error("add_child: child must be an Object")

    def remove_child(self, child: 'BaseObject', update_parent: bool = True) -> None:
        if isinstance(child, BaseObject):
            if update_parent: child._parent = None
            self.__children.remove(child)
            self._sort_children()
        else:
            Console.error("remove_child: child must be an Object")

    def update(self) -> None:
        for layer in self.__sorted_children:
            for obj in self.__sorted_children[layer]:
                obj.update()

    def draw(self, surface: pygame.Surface) -> None:
        for layer in self.__sorted_children:
            for obj in self.__sorted_children[layer]:
                obj.draw(surface)