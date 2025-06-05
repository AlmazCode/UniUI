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

        self.transform.width = 200
        self.transform.height = 200
    
    def update(self) -> None:
        super().update()
        self.text = f"FPS: {screen.fps}\nHello, World!\nline №3"
        self.transform.rotation += 100 * Time.delta_time

text_middle = CustomText(name="text_middle", font_size=22, position=Vector2(0, 0),
                         font=font_path, align=Align.MIDDLE, text_align=TextAlign.MIDDLE,
                         padding=50, rotation=45)

text_left = CustomText(name="text_left", parent=text_middle, font_size=22, position=Vector2(0, 0),
                       font=font_path, align=Align.LEFT, text_align=TextAlign.MIDDLE,
                       padding=50, rotation=45)

text_right = CustomText(name="text_right", parent=text_left, font_size=22, position=Vector2(0, 0),
                        font=font_path, align=Align.RIGHT, text_align=TextAlign.MIDDLE,
                        padding=50, rotation=45)


text_top = CustomText(name="text_top", parent=text_right, font_size=22, position=Vector2(0, 0),
                      font=font_path, align=Align.TOP, text_align=TextAlign.MIDDLE,
                      padding=50, rotation=45)

text_bottom = CustomText(name="text_bottom", parent=text_top, font_size=22, position=Vector2(0, 0),
                         font=font_path, align=Align.BOTTOM, text_align=TextAlign.MIDDLE,
                         padding=50, rotation=45)

text_topleft = CustomText(name="text_topleft", parent=text_bottom, font_size=22, position=Vector2(0, 0),
                          font=font_path, align=Align.TOPLEFT, text_align=TextAlign.MIDDLE,
                          padding=50, rotation=45)

text_topright = CustomText(name="text_topright", parent=text_topleft, font_size=22, position=Vector2(0, 0),
                           font=font_path, align=Align.TOPRIGHT, text_align=TextAlign.MIDDLE,
                           padding=50, rotation=45)

text_bottomleft = CustomText(name="text_bottomleft", parent=text_topright, font_size=22, position=Vector2(0, 0),
                             font=font_path, align=Align.BOTTOMLEFT, text_align=TextAlign.MIDDLE,
                             padding=50, rotation=45)

text_bottomright = CustomText(name="text_bottomright", parent=text_bottomleft, font_size=22, position=Vector2(0, 0),
                              font=font_path, align=Align.BOTTOMRIGHT, text_align=TextAlign.MIDDLE,
                              padding=50, rotation=45)

screen.start()