from distutils.command.config import config
from common import events, types
from common.config import DISPLAY_SCALING, FONT, TRANSISTION_SPEED, get_window_size
from session import Session
from pygame import event as pg_event, font as pg_font


class PreLoadScr:
    def __init__(self, session: Session, objective: types.Items) -> None:
        self.objective = objective
        self.bg_offset_y = 0
        self.items_count = len(session.level_data[self.objective.name]["Items"])
        self.frame_size = (session.preloader_frame.get_width(), session.preloader_frame.get_height())
        self.step = 0
        self.font = pg_font.Font(FONT[0], FONT[1])
    def update(self, session: Session, display):
        self.step = 0
        display.fill((0, 0, 0))
        if self.bg_offset_y > -170:
            display.blit(session.preloader_bg, (0, self.bg_offset_y))
            self.bg_offset_y -= 0.5
        else:
            display.blit(session.preloader_bg, (0, self.bg_offset_y))

        display.blit(
            session.preloader_frame,
            (
                (get_window_size()[0] - session.preloader_frame.get_width()) / 2,
                (get_window_size()[1] - session.preloader_frame.get_height()) / 2,
            ),
        )
        for key in session.level_data[self.objective.name]["Items"]:
            display.blit(
                session.collectibles[key.upper()],
                (
                    ((self.frame_size[0] / self.items_count) - session.collectibles[key.upper()].get_width()) / 2 + (self.frame_size[0] / self.items_count * self.step) + ((get_window_size()[0] - session.preloader_frame.get_width()) / 2),
                    280 * DISPLAY_SCALING
                )
                
            )
            self.step += 1
