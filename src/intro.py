import json, pygame
class Intro():
    def __init__(self):
        from pathlib import Path
        from common import paths
        from common import utils

        self.dialogue_path = paths.DATA_PATH / "dialogues.json"
        self.background_path = paths.ASSETS_PATH / "background"
        self.intro_scenes_path = paths.ASSETS_PATH / "intro_scenes"
        self.intro_scenes = tuple(map(utils.load_img, Path(self.intro_scenes_path).glob("*.png")))
        self.alpha = 0
        with open(self.dialogue_path) as r:
            self.intro_lines = json.load(r)["intro_story"]
        self.page_count = len(self.intro_lines)
        self.current_page = 0
    def jumpto(self, page):
        self.current_page = page
    def flip(self):
        self.current_page += 1
    def show(self, display: pygame.surface.Surface):
        from common import config
        display.fill((0, 0, 0))
        current_scene = self.intro_scenes[self.current_page]
        if self.alpha <= 255:
            self.alpha += config.TRANSISTION_SPEED
            current_scene.set_alpha(self.alpha)
        display.blit(current_scene, (0, 0))
