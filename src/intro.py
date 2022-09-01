import json, pygame
from common import events
from common.config import CLICK_PROMPT, DISPLAY_SCALING, get_window_size

from common.utils import drawText


class Intro:
    def __init__(self):
        from pathlib import Path
        from common import paths
        from common import utils

        self.dialogue_path = paths.DATA_PATH / "dialogues.json"
        self.background_path = paths.ASSETS_PATH / "background"
        self.intro_scenes_path = paths.ASSETS_PATH / "intro_scenes"
        self.intro_scenes = tuple(
            map(utils.load_img, Path(self.intro_scenes_path).glob("*.png"))
        )
        self.alpha = 0
        with open(self.dialogue_path) as r:
            self.intro_lines = json.load(r)["intro_story"]
        self.page_count = len(self.intro_lines)
        self.current_page = 0

    def jumpto(self, page):
        self.current_page = page

    def flip(self):
        self.alpha = 0
        from common.events import PLAY

        if self.current_page < self.page_count - 1:
            self.current_page += 1
        else:
            pygame.event.post(pygame.event.Event(PLAY))

    def update(self, display: pygame.surface.Surface):
        from common import config

        if self.current_page < self.page_count - 1:
            # draw image
            if self.current_page == 0:
                display.fill((0, 0, 0))
            else:
                display.blit(self.intro_scenes[self.current_page - 1], (0, 0))

            current_scene = self.intro_scenes[self.current_page]
            if self.alpha < 255:
                self.alpha += config.TRANSISTION_SPEED
            elif self.alpha >= 255:
                self.alpha = 255
            current_scene.set_alpha(self.alpha)
            display.blit(current_scene, (0, 0))
            display.blit(
                CLICK_PROMPT, (get_window_size()[0] - CLICK_PROMPT.get_width() - 20, 20)
            )

            # draw text
            textRect = pygame.rect.Rect(
                20,
                812.28 * DISPLAY_SCALING + 20,
                (1558 * DISPLAY_SCALING) - 20,
                (149 * DISPLAY_SCALING) - 20,
            )
            drawText(
                display,
                self.intro_lines[self.current_page],
                (255, 255, 255),
                textRect,
                pygame.font.Font(config.FONT[0], config.FONT[1]),
            )
        else:
            pygame.event.post(pygame.event.Event(events.INTRODUCTION_DIALOGUE))
