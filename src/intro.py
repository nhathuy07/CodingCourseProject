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
        self.page_count = len(self.intro_scenes)
        self.current_page = 0
    def jumpto(self, page):
        self.current_page = page
    def flip(self):
        from common.events import PLAY
        if self.current_page < self.page_count - 1:
            self.current_page += 1
        else:
            pygame.event.post(pygame.event.Event(PLAY))
        self.alpha = 0
    def show(self, display: pygame.surface.Surface):
        from common import config
        
        if self.current_page == 0:
            display.fill((0, 0, 0))
        else:
            display.blit(self.intro_scenes[self.current_page - 1], (0, 0))
        current_scene = self.intro_scenes[self.current_page]
        if self.alpha <= 255:
            self.alpha += config.TRANSISTION_SPEED
            current_scene.set_alpha(self.alpha)
        display.blit(current_scene, (0, 0))
