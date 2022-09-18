import json, pygame

from common import events
from common.config import DISPLAY_SCALING, get_window_size

from common.utils import drawText
from session import Session


class Intro():
    def __init__(self, pre_bossfight = False, is_outro = False):
        from pathlib import Path
        from common import paths
        from common import utils
        pygame.mixer.init()
        self.pre_bossfight = pre_bossfight
        self.alpha = 0

        self.dialogue_path = paths.DATA_PATH / "dialogues.json"
        # load intro for the beginning of the game
        if not pre_bossfight:
            
            self.background_path = paths.ASSETS_PATH / "background"
            self.intro_scenes_path = paths.ASSETS_PATH / "intro_scenes"
            self.intro_scenes = tuple(
                map(utils.load_img, Path(self.intro_scenes_path).glob("*.png"))
            )
            with open(self.dialogue_path) as r:
                data = json.load(r)
                self.intro_lines = data["intro_story"]
                self.sound_sequence = data["intro_sound_sequence"]
        else:

            # load intro for boss level
            self.intro_scenes_path = paths.ASSETS_PATH / "preboss_scenes"
            self.intro_scenes = tuple(
                map(utils.load_img, Path(self.intro_scenes_path).glob("*.png"))
            )
            with open(self.dialogue_path) as r:
                data = json.load(r)
                self.intro_lines = data["boss_fight"]["intro"]
                self.sound_sequence = data["boss_fight"]["audio_sequence"]

       

        # EXTRA: Outro data
        self.is_outro = is_outro
        if self.is_outro:
            with open(self.dialogue_path) as r:
                    data = json.load(r)
                    self.intro_lines = data["outro"]
                    self.sound_sequence = data["outro_audio_sequence"]

        self.page_count = len(self.intro_lines)
        self.current_page = 0
        self.current_sound = None
        self.sound_played = False


    def jumpto(self, page):
        self.current_page = page

    def flip(self):
        self.sound_played = False
        self.current_sound.stop()
        self.alpha = 0

        if self.current_page < self.page_count - 1:
            self.current_page += 1
        else:
            if not self.pre_bossfight and not self.is_outro:
                self.current_sound.stop()
                pygame.event.post(pygame.event.Event(events.INTRODUCTION_DIALOGUE))
            elif self.pre_bossfight and not self.is_outro:
                self.current_sound.stop()
                pygame.event.post(pygame.event.Event(events.BOSS_LVL_DIALOGUE))
            else:
                pygame.event.post(pygame.event.Event(events.ABOUT))
            

    def update(self, display: pygame.surface.Surface, session: Session):
        from common import config
        if not self.sound_played:
            self.current_sound = session.sfx[self.sound_sequence[self.current_page]]
            self.current_sound.play()
            self.sound_played = True

        if self.current_page <= self.page_count - 1:
            # draw image
            if self.current_page == 0:
                display.fill((0, 0, 0))
            else:
                display.blit(self.intro_scenes[self.current_page - 1], (0, 0))

            if not self.is_outro:
                current_scene = self.intro_scenes[self.current_page]
            else:
                current_scene = session.OUTRO

            if self.alpha < 255:
                self.alpha += config.TRANSISTION_SPEED
            elif self.alpha >= 255:
                self.alpha = 255
            current_scene.set_alpha(self.alpha)
            display.blit(current_scene, (0, 0))
            display.blit(
                session.CLICK_PROMPT,
                (get_window_size()[0] - session.CLICK_PROMPT.get_width() - 20, 20),
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

