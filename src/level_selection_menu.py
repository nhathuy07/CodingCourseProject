from pygame import event as pg_event
from pygame import font as pg_font
from pygame import mouse as pg_mouse
from pygame import display as pg_disp
from pygame import MOUSEBUTTONDOWN, QUIT
from common.types import Items
from session import Session
from common import config, events
from ctypes import windll

messageBox = windll.user32.MessageBoxW

from session import Session


class LvSelection:
    def __init__(self) -> None:
        self.prompt_font = pg_font.Font(config.FONT[0], int(config.FONT[1] * 1.5))
        self.prompt = self.prompt_font.render(
            "Which item do you want to collect?", True, (99, 61, 17), None
        )
        self.alpha = 0

    def update(self, session: Session, display):

        if self.alpha <= 255:
            self.alpha += config.TRANSISTION_SPEED
            display.fill((0, 0, 0))
            bg = session.lv_selection_bg
            bg.set_alpha(self.alpha)
            display.blit(bg, (0, 0))
        else:
            display.blit(session.lv_selection_bg, (0, 0))

            display.blit(
                config.ITEM_PANE,
                (351.45 * config.DISPLAY_SCALING, 764.2 * config.DISPLAY_SCALING),
            )
            display.blit(
                self.prompt,
                (
                    (config.get_window_size()[0] - self.prompt.get_width()) / 2,
                    115.84 * config.DISPLAY_SCALING,
                ),
            )
            for i in range(Items.__len__()):
                if Items._member_names_[i] in session.playerData["earned_items"]:
                    display.blit(
                        session.game_items[Items._member_names_[i]][0],
                        (
                            session.game_items["positions"][i][0]
                            * config.DISPLAY_SCALING,
                            session.game_items["positions"][i][1]
                            * config.DISPLAY_SCALING,
                        ),
                    )
                else:
                    display.blit(
                        session.game_items[Items._member_names_[i]][1],
                        (
                            session.game_items["positions"][i][0]
                            * config.DISPLAY_SCALING,
                            session.game_items["positions"][i][1]
                            * config.DISPLAY_SCALING,
                        ),
                    )
            for e in pg_event.get(MOUSEBUTTONDOWN, QUIT):
                if e.type == MOUSEBUTTONDOWN:
                    for item in Items._member_names_:
                        if session.rects[item].collidepoint(pg_mouse.get_pos()):
                            if item in session.playerData["earned_items"]:
                                messageBox(
                                    0,
                                    "There's no need to collect an item twice!",
                                    "Message",
                                    0x40,
                                )
                            else:
                                pg_event.post(pg_event.Event(Items[item].value))
