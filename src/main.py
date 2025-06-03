import pygame
from UniUI import Screen, Vector2, Text, Time, Align, TextAlign
from pathlib import Path

screen = Screen(resolution = Vector2(1280, 720), title = "Test App", flags = pygame.DOUBLEBUF)

font_path = Path(__file__).parent / "assets" / "FiraCode-Regular.ttf"

class CustomText(Text):
    def __init__(self, *, name: str, **args) -> None:
        super().__init__(name, **args)
    
    def update(self) -> None:
        super().update()
        self.text = f"FPS: {screen.fps}\nHello, World!"

text = CustomText(name = "text", font_size = 72, position = Vector2(0, 0),
                  font = font_path,
                  align = Align.MIDDLE, text_align = TextAlign.MIDDLE)

screen.start()