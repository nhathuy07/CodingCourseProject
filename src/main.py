
import pygame
from intro import Intro
from mainMenu import MainMenu
from common import config
from common import events
from session import Session

import ctypes
MessageBox = ctypes.windll.user32.MessageBoxW

def menu(session):
    display = pygame.display.set_mode(config.get_window_size())
    mainMenu = MainMenu(session=session, display=display)
    user_in_menu = True
    while user_in_menu:
        mainMenu.run([e for e in pygame.event.get()])
        eventList = [ev.type for ev in pygame.event.get((events.ABOUT, events.HELP, events.PLAY, events.RESUME))]
        if len(eventList) != 0:
            user_in_menu = False
        else:
            pygame.display.flip()
    return eventList

def intro():
    display = pygame.display.set_mode(config.get_window_size())
    clock = pygame.time.Clock()
    
    intro = Intro()
    intro_ended = False
    while not intro_ended:
        for ev in pygame.event.get((pygame.QUIT, pygame.MOUSEBUTTONDOWN, events.MAIN_MENU, events.PLAY)):
            if ev.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(events.MAIN_MENU))
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                intro.flip()
            else:
                return ev.type
        intro.show(display)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    session = Session()

    while True:
        pygame.event.clear()
        menu_instance = menu(session)
        if events.PLAY in menu_instance:
            intro_instance = intro()
            if intro_instance == events.PLAY:
                print("Entering game...")
            elif intro_instance == events.MAIN_MENU:
                continue
        elif events.ABOUT in menu_instance:
            MessageBox(None, "Demo", "Demo", 0)
