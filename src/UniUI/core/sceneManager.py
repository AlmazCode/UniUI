from typing import Callable
from .scene import Scene

class SceneManager:
    def __init__(self) -> None:
        self.scenes: dict[str, Scene] = {}
        self.active_scene: Scene = None
        
    def scene(self, name):
        def decorator(init_func: Callable[[Scene], None]) -> Scene:
            scene = Scene(name, init_func)
            self.scenes[name] = scene
            return scene
        return decorator
        
    def load_scene(self, name: str) -> None:
        if self.active_scene:
            self.active_scene.unload()
            
        scene = self.scenes.get(name)
        if scene:
            self.active_scene = scene
            scene.load()