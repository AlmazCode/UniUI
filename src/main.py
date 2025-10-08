import pygame
from UniUI import Screen, Scene, Vector2, Text, Align, TextAlign, SceneManager
from pathlib import Path

screen = Screen(resolution = Vector2(1280, 720), title = "Test App", pg_flags = pygame.DOUBLEBUF)
manager = SceneManager()

font_path = Path(__file__).parent / "assets" / "FiraCode-Regular.ttf"

class CustomText(Text):
    def __init__(self, *, name: Scene, scene: str, **args) -> None:
        super().__init__(name, scene, **args)

        self.transform.width = 200
        self.transform.height = 200
    
    def update(self) -> None:
        super().update()
        self.text = f"FPS: {Screen.Instance.fps}\nHello, World!\nline №3"
        # self.transform.width += 1
        # self.transform.rotation += 100 * Screen.Time.delta_time
        self.transform.scale.x += 0.005
        self.transform.scale.y += 0.005

@manager.scene("main")
def main(scene: Scene) -> None:
    text_middle = CustomText(name="text_middle", scene=scene, font_size=22, position=Vector2(0, 0),
                            font=font_path, align=Align.MIDDLE, text_align=TextAlign.MIDDLE,
                            padding=0, rotation=0)
    return
    text_left = Text(name="text_left", scene=scene, parent=text_middle, font_size=22, position=Vector2(0, 0),
                        font=font_path, align=Align.LEFT, text_align=TextAlign.MIDDLE,
                        padding=50, rotation=0)

    text_right = Text(name="text_right", scene=scene, parent=text_middle, font_size=22, position=Vector2(0, 0),
                            font=font_path, align=Align.RIGHT, text_align=TextAlign.MIDDLE,
                            padding=50, rotation=0)

    text_top = Text(name="text_top", scene=scene, parent=text_middle, font_size=22, position=Vector2(0, 0),
                        font=font_path, align=Align.TOP, text_align=TextAlign.MIDDLE,
                        padding=50, rotation=0)

    text_bottom = Text(name="text_bottom", scene=scene, parent=text_middle, font_size=22, position=Vector2(0, 0),
                            font=font_path, align=Align.BOTTOM, text_align=TextAlign.MIDDLE,
                            padding=50, rotation=0)

    text_topleft = Text(name="text_topleft", scene=scene, parent=text_middle, font_size=22, position=Vector2(0, 0),
                            font=font_path, align=Align.TOPLEFT, text_align=TextAlign.MIDDLE,
                            padding=50, rotation=0)

    text_topright = Text(name="text_topright", scene=scene, parent=text_middle, font_size=22, position=Vector2(0, 0),
                            font=font_path, align=Align.TOPRIGHT, text_align=TextAlign.MIDDLE,
                            padding=50, rotation=0)

    text_bottomleft = Text(name="text_bottomleft", scene=scene, parent=text_middle, font_size=22, position=Vector2(0, 0),
                                font=font_path, align=Align.BOTTOMLEFT, text_align=TextAlign.MIDDLE,
                                padding=50, rotation=0)

    text_bottomright = Text(name="text_bottomright", scene=scene, parent=text_middle, font_size=22, position=Vector2(0, 0),
                                font=font_path, align=Align.BOTTOMRIGHT, text_align=TextAlign.MIDDLE,
                                padding=50, rotation=0)

manager.load_scene("main")