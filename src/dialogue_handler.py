import pygame
from common import config, events, utils
from common.extra_types import Levels
from common.paths import ASSETS_PATH
from session import Session


class Dialogue:
    def __init__(self, session: Session, pg_range: tuple[int, int], pre_bossfight = False, bossfight = False) -> None:
        from common import paths
        from pathlib import Path

        self.range = pg_range
        self.dialog_list = session.dialogue_data["dialogues"]
        self.line = 0
        self.section = 0
        self.dialogue_scenes = session.dialogue_scenes
        self.dialogue_surface = pygame.surface.Surface(
            (config.DIALOG_DISP_AREA.width, config.DIALOG_DISP_AREA.height)
        )
        self.alpha = -255
        self.next_section_ev_posted = False
        self.set_section(self.range[0])

        self.current_sound = None
        self.sound_played = False

        self.pre_bossfight = pre_bossfight
        self.bossfight = bossfight

        pygame.mixer.music.load(ASSETS_PATH / "sfx" / "mainmenu_2.wav")
        pygame.mixer.music.play()
        
    def next_line(self):
        self.line += 1
        self.current_sound.stop()
        self.sound_played = False

    def set_section(self, s: int):
        self.section = s
        self.next_section_ev_posted = False
        self.alpha = -255
        self.line = 0

    def update(self, display, session: Session):
        #self.sound.play()

        if self.line < len(self.dialog_list[self.section]):
            from common import config

            display.fill((0, 0, 0))

            section_data = self.dialog_list[self.section][self.line]

            if not self.sound_played:
                self.current_sound = session.sfx[f"{section_data['speaker']}.wav".lower()]
                self.current_sound.play()
                self.sound_played = True

            if -255 <= self.alpha < 0:
                current_bg = (
                    self.dialogue_scenes[self.section - 1]
                    if self.section > 0
                    else self.dialogue_scenes[self.section]
                )
                current_bg.set_alpha(abs(self.alpha))
                self.alpha += config.TRANSISTION_SPEED
            else:
                current_bg = self.dialogue_scenes[self.section]
                current_bg.set_alpha((self.alpha))
                self.alpha += config.TRANSISTION_SPEED

            display.blit(current_bg, (0, 0))
            if self.alpha >= 255:
                self.speakerName = pygame.font.Font(
                    config.FONT[0], config.FONT[1]
                ).render(section_data["speaker"], True, (255, 178, 71))
                self.avatar = session.avatars[section_data["speaker"]]

                display.blit(
                    self.avatar,
                    (
                        config.get_window_size()[0] - self.avatar.get_width(),
                        config.get_window_size()[1] - self.avatar.get_height(),
                    ),
                )

                display.blit(
                    self.speakerName,
                    (
                        config.DIALOG_DISP_AREA.left + 10,
                        config.DIALOG_DISP_AREA.top - self.speakerName.get_height(),
                    ),
                )

                utils.drawText(
                    display,
                    section_data["line"],
                    (255, 255, 255),
                    pygame.rect.Rect(
                        config.DIALOG_DISP_AREA.left + 10,
                        config.DIALOG_DISP_AREA.top + 10,
                        config.DIALOG_DISP_AREA.width - 20,
                        config.DIALOG_DISP_AREA.height - 20,
                    ),
                    pygame.font.Font(config.FONT[0], config.FONT[1]),
                )
                display.blit(
                    session.CLICK_PROMPT,
                    (
                        config.get_window_size()[0]
                        - session.CLICK_PROMPT.get_width()
                        - 20,
                        20,
                    ),
                )
        elif self.section < self.range[1]:
            self.set_section(self.section + 1)
        else:

            if not self.pre_bossfight:
                if not self.bossfight:
                    pygame.event.post(pygame.event.Event(events.GO_TO_LV_SELECTION))
                else:
                    pygame.event.post(pygame.event.Event(Levels.BOSS.value))
            
            elif self.pre_bossfight:
                pygame.event.post(pygame.event.Event(events.BOSS_LVL_INTRO))
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            
