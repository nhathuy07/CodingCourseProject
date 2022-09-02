from common.types import Items, Levels
from preload_scr import PreLoadScr
from session import Session
from mainMenu import MainMenu
from intro import Intro
from dialogue_handler import Dialogue
from level_selection_menu import LvSelection
import pygame
from common import config, events

# load event codes
commonEvents = (
    events.PLAY,
    events.RESUME,
    events.ABOUT,
    pygame.MOUSEBUTTONDOWN,
    pygame.QUIT,
    events.INTRODUCTION_DIALOGUE,
    events.GO_TO_LV_SELECTION,
    events.PRELOAD_SCREEN,
)
preloaderCode = [x.value for x in Items]
levelCode = [x.value for x in Items]



if __name__ == "__main__":
    session = Session()
    display = pygame.display.set_mode(config.get_window_size())
    clock = pygame.time.Clock()
    current_screen = MainMenu(session, display)
    while True:
        # update screens
        if type(current_screen).__name__ == "MainMenu":
            pygame.event.set_allowed(commonEvents)
            current_screen.update([e for e in pygame.event.get()])
        elif type(current_screen).__name__ == "Intro":
            current_screen.update(display)
        elif type(current_screen).__name__ == "Dialogue":
            current_screen.update(display, session)
        elif type(current_screen).__name__ == "LvSelection":
            current_screen.update(session, display)
        elif type(current_screen).__name__ == "PreLoadScr":
            current_screen.update(session, display)




        for e in pygame.event.get(eventtype=(*commonEvents, *levelCode, *preloaderCode)):
            if e.type == events.PLAY:
                session.override_savefile()
                current_screen = Intro()
                pygame.event.set_allowed((pygame.MOUSEBUTTONDOWN, events.INTRODUCTION_DIALOGUE, pygame.QUIT, events.EXIT))
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if type(current_screen).__name__ == "Intro":
                    current_screen.flip()
                elif type(current_screen).__name__ == "Dialogue":
                    current_screen.next_line()
                    current_screen.update(display, session)

            elif e.type == events.INTRODUCTION_DIALOGUE:
                current_screen = Dialogue(session, (0, 1))
                pygame.event.set_allowed((pygame.QUIT, events.EXIT, events.GO_TO_LV_SELECTION, pygame.MOUSEBUTTONDOWN))
            elif e.type == events.GO_TO_LV_SELECTION:
                current_screen = LvSelection()
                pygame.event.set_allowed((pygame.QUIT, events.PRELOAD_SCREEN, *preloaderCode, pygame.MOUSEBUTTONDOWN))

            elif e.type == events.RESUME:
                current_screen = LvSelection()
                pygame.event.set_allowed((pygame.QUIT, events.PRELOAD_SCREEN, *preloaderCode, pygame.MOUSEBUTTONDOWN))
            elif e.type in preloaderCode:
                current_screen = PreLoadScr(session, Items(e.type))
                pygame.event.set_allowed((pygame.QUIT, pygame.MOUSEBUTTONDOWN, *levelCode))
            elif e.type == pygame.QUIT:
                quit()

        pygame.display.flip()
        clock.tick(120)
