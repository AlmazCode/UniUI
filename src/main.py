from UniUI import *

import pygame.freetype

from pathlib import Path

# creating most important objects
screen = Screen(
    resolution = Vector2(1280, 720),
    title = "Test App",
    pg_flags = pygame.DOUBLEBUF | pygame.RESIZABLE,
    priority=0.5
)
manager = SceneManager()

# loading font
font_path = Path(__file__).parent / "assets" / "FiraCode-Regular.ttf"
font = pygame.freetype.Font(font_path)

# creating custom Text class to control our text
class CustomText(Text):
    def __init__(self, *, name: Scene, scene: str, **args) -> None:
        super().__init__(name, scene, **args)

        self.transform.width = 200
        self.transform.height = 200
    
    def update(self) -> None:
        super().update()
        self.text = f"FPS: {Screen.fps()}\nHello, World!\nline №3"
        # self.transform.width += 1
        # self.transform.rotation += 100 * Screen.Time.delta_time
        # self.transform.scale.x += 0.005
        # self.transform.scale.y += 0.001
        # self.font_size += 0.1

# creating main scene
@manager.scene("main")
def main(scene: Scene) -> None:

    text_middle = CustomText(
        name="text_middle",
        scene=scene,
        font_size=22,
        position=Vector2(0, 0),
        font=font,
        align=Align.MIDDLE,
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50,
        rotation=0
    )

    text_left = Text(
        name="text_left",
        scene=scene,
        parent=None,
        font_size=22,
        position=Vector2(0, 0),
        font=font,
        align=Align.LEFT,
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50,
        rotation=45,
        width=200,
        height=200
    )

    text_right = Text(
        name="text_right",
        scene=scene,
        parent=None, 
        font_size=22, 
        position=Vector2(0, 0),
        font=font,
        align=Align.RIGHT,
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50,
        rotation=45,
        width=200, 
        height=200
    )

    text_top = Text(
        name="text_top",
        scene=scene,
        parent=None,
        font_size=22,
        position=Vector2(0, 0),
        font=font, 
        align=Align.TOP, 
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50, 
        rotation=45, 
        width=200, 
        height=200
    )

    text_bottom = Text(
        name="text_bottom", 
        scene=scene, 
        parent=None,
        font_size=22, 
        position=Vector2(0, 0),
        font=font, 
        align=Align.BOTTOM, 
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50, 
        rotation=45, 
        width=200, 
        height=200
    )

    text_topleft = Text(
        name="text_topleft", 
        scene=scene, 
        parent=None, 
        font_size=22, 
        position=Vector2(0, 0),
        font=font, 
        align=Align.TOPLEFT, 
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50, 
        rotation=45, 
        width=200, 
        height=200
    )

    text_topright = Text(
        name="text_topright", 
        scene=scene, 
        parent=None, 
        font_size=22, 
        position=Vector2(0, 0),
        font=font, 
        align=Align.TOPRIGHT, 
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50, 
        rotation=45, 
        width=200, 
        height=200
    )

    text_bottomleft = Text(
        name="text_bottomleft", 
        scene=scene, 
        parent=None, 
        font_size=22, 
        position=Vector2(0, 0),
        font=font, 
        align=Align.BOTTOMLEFT, 
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50, 
        rotation=45, 
        width=200, 
        height=200
    )

    text_bottomright = Text(
        name="text_bottomright", 
        scene=scene, 
        parent=None, 
        font_size=22, 
        position=Vector2(0, 0),
        font=font, 
        align=Align.BOTTOMRIGHT, 
        text_align=TextAlign(TextAlignX.MIDDLE, TextAlignY.MIDDLE),
        padding=50, 
        rotation=45, 
        width=200, 
        height=200
    )

# loading main scene
manager.load_scene("main")