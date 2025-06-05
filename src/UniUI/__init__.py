from .core.object import BaseObject, import_screen_module
from .core.screen import Screen
from .core.time import Time as _Time
from .core.ui.color import Color
from .core.ui.text import Text
from .core.math.vector2 import Vector2
from .core.ui.transform import Transform
from .core.ui.align import Align, TextAlign
from .core import settings

Time = _Time()

import_screen_module()
del import_screen_module