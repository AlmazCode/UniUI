import pygame
import UniUI
from UniUI import Screen, Vector2, Text, Time, Align, TextAlign
from pathlib import Path

screen = Screen(resolution = Vector2(1280, 720), title = "Test App", flags = pygame.DOUBLEBUF)
UniUI.settings.DEBUG_APP = True

font_path = Path(__file__).parent / "assets" / "FiraCode-Regular.ttf"

class CustomText(Text):
    def __init__(self, *, name: str, **args) -> None:
        super().__init__(name, **args)
    
    def update(self) -> None:
        super().update()
        self.text = f"FPS: {screen.fps}\nHello, World!\nline №3"
        self.transform.rotation += 100 * Time.delta_time

text = CustomText(name = "text", font_size = 72, position = Vector2(0, 0),
                  font = font_path,
                  align = Align.MIDDLE, text_align = TextAlign.MIDDLE, padding = 50, rotation = 45)
text2 = CustomText(name = "text2", parent = text, font_size = 32, position = Vector2(0, 0),
                  font = font_path,
                  align = Align.LEFT, text_align = TextAlign.MIDDLE, padding = 50, rotation = 45)
text3 = CustomText(name = "text3", parent = text2, font_size = 32, position = Vector2(0, 0),
                  font = font_path,
                  align = Align.RIGHT, text_align = TextAlign.MIDDLE, padding = 50, rotation = 45)
text2.parent = None
text3.active = False
text3.active = True
screen.start()