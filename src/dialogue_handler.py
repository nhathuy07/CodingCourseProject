import pygame
from common import config, utils
from common.paths import ASSETS_PATH
from session import Session

class Dialogue():
    def __init__(self, dialog_list) -> None:
        from common import paths
        from pathlib import Path
        self.dialog_list = dialog_list["dialogues"]
        self.line = 0
        self.section = 0
        self.dialogue_scenes_path = paths.ASSETS_PATH / "dialogue_scenes"
        self.dialogue_scenes = tuple(map(utils.load_img, Path(self.dialogue_scenes_path).glob("*.png")))
        self.dialog_surface = pygame.surface.Surface((config.DIALOG_DISP_AREA.width, config.DIALOG_DISP_AREA.height))
        
    def next_line(self):
        self.line += 1
    def set_section(self, s):
        self.section = s
    def show(self, display: pygame.display, session: Session, section = 0):
        
        from common import paths, config

        section_data = self.dialog_list[section][self.line]
        display.blit(self.dialogue_scenes[self.section], (0,0))
        self.speakerName = pygame.font.Font(config.FONT[0], config.FONT[1]).render(section_data["speaker"], True, (255, 178, 71))
        self.avatar = session.avatars[section_data["speaker"]]
        
        display.blit(self.avatar, (config.get_window_size()[0] - self.avatar.get_width(), config.get_window_size()[1] - self.avatar.get_height()))

        display.blit(self.speakerName, (config.DIALOG_DISP_AREA.left + 10, config.DIALOG_DISP_AREA.top - self.speakerName.get_height()))
        utils.drawText(
            display,
            section_data["line"], 
            (255, 255, 255),
            pygame.rect.Rect(config.DIALOG_DISP_AREA.left + 10, config.DIALOG_DISP_AREA.top + 10, config.DIALOG_DISP_AREA.width - 20, config.DIALOG_DISP_AREA.height - 20),
            pygame.font.Font(config.FONT[0], config.FONT[1]))
        
    