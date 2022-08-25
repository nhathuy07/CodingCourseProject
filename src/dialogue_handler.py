import pygame
from common import config

class Dialogue():
    def __init__(self, dialog_list) -> None:
        self.dialog_list = dialog_list
        self.line = 0
    def next_line(self):
        self.line += 1
    def show(self):
        pygame.surface.Surface()
        pygame.draw.rect(pygame.surface.Surface((config.DIALOG_DISP_AREA.width, config.DIALOG_DISP_AREA.height)), (0, 0, 0, 140), config.DIALOG_DISP_AREA, border_radius=5)
        