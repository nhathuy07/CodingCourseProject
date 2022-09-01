from pygame_menu import Menu, themes, events as pg_menu_events
import pygame as pg
from common.types import MenuOption
from common import events
from common.config import get_window_size
from session import Session

pg.init()


class MainMenu:
    def __init__(self, session: Session, display):
        session.load_or_create_savefile()
        self.display = display
        self.menu = Menu(
            "RoboMiner",
            get_window_size()[0],
            get_window_size()[1],
            theme=themes.THEME_DARK,
        )
        self.choosen = None
        if len(session.playerData["earned_items"]) == 0:
            self.menu.add.button(
                "Start Game", action=lambda: pg.event.post(pg.event.Event(events.PLAY))
            )
        else:
            self.menu.add.button(
                "Resume Game",
                action=lambda: pg.event.post(pg.event.Event(events.RESUME)),
            )
            self.menu.add.button(
                "Start Over", action=lambda: pg.event.post(pg.event.Event(events.PLAY))
            )
        self.menu.add.button(
            "Help", action=lambda: pg.event.post(pg.event.Event(events.HELP))
        )
        self.menu.add.button(
            "About", action=lambda: pg.event.post(pg.event.Event(events.ABOUT))
        )
        self.menu.add.button("Exit", pg_menu_events.EXIT)

    def update(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.display)

    def reset(self):
        self.choosen = None

    def goto(self, part):
        self.choosen = part
