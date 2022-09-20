from platform import platform, system
from pygame import event as pg_event
from pygame import font as pg_font
from pygame import mouse as pg_mouse
from pygame import MOUSEBUTTONDOWN, QUIT, K_ESCAPE
from pygame import key as pg_key
from common.extra_types import Items
from session import Session
from common import config, events
from ctypes import windll
from aquaui import AlertType, Alert, Buttons

messageBox = windll.user32.MessageBoxW

from session import Session


class LvSelection():
    def __init__(self) -> None:
        self.prompt_font = pg_font.Font(config.FONT2[0], int(config.FONT2[1] * 1.5))
        self.prompt = self.prompt_font.render(
            "Which item do you want to collect?", True, (99, 61, 17), None
        )
        self.alpha = 0
        self.sound = None
    def update(self, session: Session, display):
        if session.base_level_completed():
            pg_event.post(pg_event.Event(events.PRE_BOSS_LVL_DIALOGUE))

        else:
            self.sound = session.sfx["mainmenu_2.wav"]
            self.sound.set_volume(0.2)
            self.sound.play()
            if self.alpha <= 255:
                self.alpha += config.TRANSISTION_SPEED
                display.fill((0, 0, 0))
                bg = session.lv_selection_bg
                bg.set_alpha(self.alpha)
                display.blit(bg, (0, 0))
            else:
                display.blit(session.lv_selection_bg, (0, 0))

                display.blit(
                    session.ITEM_PANE,
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
                        self.sound.stop()
                        for item in Items._member_names_:
                            if session.rects[item].collidepoint(pg_mouse.get_pos()):
                                if item in session.playerData["earned_items"]:
                                    if system() == "Windows":
                                        messageBox(
                                            0,
                                            "There's no need to collect an item twice!",
                                            "Message",
                                            0x40,
                                        )
                                    elif system() == "Darwin":
                                        alert = Alert("There's no need to collect an item twice!").of_type(AlertType.INFORMATIONAL).show()
                                else:
                                    self.sound = session.sfx["click.wav"]
                                    self.sound.play()
                                    pg_event.post(pg_event.Event(Items[item].value))
                if pg_key.get_pressed()[K_ESCAPE]:
                    pg_event.post(pg_event.Event(events.MAIN_MENU))
                    self.sound.stop()