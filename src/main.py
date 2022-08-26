
import pygame
from dialogue_handler import Dialogue
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

def intro(session: Session):
    display = pygame.display.set_mode(config.get_window_size())
    clock = pygame.time.Clock()
    
    intro = Intro()
    dialogue = Dialogue(session.dialogue_data)
    intro_ended = False
    dialogue_ended = False
    while not intro_ended:
        for ev in pygame.event.get((pygame.QUIT, pygame.MOUSEBUTTONDOWN, events.MAIN_MENU, events.PLAY)):
            if ev.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(events.MAIN_MENU))
                dialogue_ended = True
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                intro.flip()
            else:
                intro_ended = True
        intro.show(display)
        pygame.display.flip()
        clock.tick(60)


    while not dialogue_ended:
        #display.fill((0, 0, 0))
        
        for ev in pygame.event.get((pygame.QUIT, pygame.MOUSEBUTTONDOWN, events.MAIN_MENU, events.PLAY)):
            if ev.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(events.MAIN_MENU))
                dialogue_ended = True
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                dialogue.next_line()
            else:
                return ev.type
        
        dialogue.show(display, session, section=0)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    session = Session()

    while True:
        pygame.event.clear()
        menu_instance = menu(session)
        if events.PLAY in menu_instance:
            intro_instance = intro(session)
            if intro_instance == events.PLAY:
                print("Entering game...")
            elif intro_instance == events.MAIN_MENU:
                continue
        elif events.ABOUT in menu_instance:
            MessageBox(None, "Demo", "Demo", 0)
