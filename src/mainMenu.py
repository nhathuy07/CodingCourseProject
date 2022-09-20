from pygame_menu import Menu, themes
import pygame as pg
from common import events
from common.config import get_window_size
from session import Session
from pygame import QUIT

pg.init()
pg.mixer.init()

class MainMenu:
    def __init__(self, session: Session, display):
        session.load_or_create_savefile()
        session.sfx["mainmenu.wav"].set_volume(0.2)
        
        self.display = display
        self.menu = Menu(
            "Space Miner",
            get_window_size()[0],
            get_window_size()[1],
            theme=themes.THEME_DARK,
        )
        self.choosen = None
        if session.is_newgame():
            self.menu.add.button(
                "Start Game", action=lambda: pg.event.post(pg.event.Event(events.PLAY)) 
            )
        else:
            self.menu.add.button(
                "Resume Game",
                action=lambda: pg.event.post(pg.event.Event(events.RESUME)) 
            )
            self.menu.add.button(
                "Start Over", action=lambda: pg.event.post(pg.event.Event(events.PLAY)) 
            )
        self.menu.add.button(
            "About", action=lambda: pg.event.post(pg.event.Event(events.ABOUT))
        )
        self.menu.add.button("Exit", action=lambda: pg.event.post(pg.event.Event(QUIT)))

    def update(self, events, session: Session):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.display)
            session.sfx["mainmenu.wav"].play()
