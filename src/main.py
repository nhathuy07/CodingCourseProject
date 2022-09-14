import ctypes
from common.types import Items, Levels, Scheme
from mission_completed import MissionCompletedScr
from preload_scr import PreLoadScr
from session import Session
from mainMenu import MainMenu
from intro import Intro
from dialogue_handler import Dialogue
from level_selection_menu import LvSelection
import pygame
from common import config, events
from world import World

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
    events.MISSION_COMPLETED,
    pygame.KEYDOWN,
)
preloaderCode = [x.value for x in Items]
levelCode = [x.value for x in Levels]


if __name__ == "__main__":
    session = Session()
    display = pygame.display.set_mode(config.get_window_size(), pygame.HWACCEL)
    clock = pygame.time.Clock()
    current_screen = MainMenu(session, display)
    common_events_allowed = False
    while True:
        # update screens
        if type(current_screen).__name__ == "MainMenu":
            if not common_events_allowed:
                pygame.event.set_allowed(commonEvents)
                common_events_allowed = True
            current_screen.update([e for e in pygame.event.get()])
        elif type(current_screen).__name__ == "Intro":
            common_events_allowed = False
            current_screen.update(display, session)
        elif type(current_screen).__name__ == "Dialogue":
            common_events_allowed = False
            current_screen.update(display, session)
        elif type(current_screen).__name__ == "LvSelection":
            common_events_allowed = False
            current_screen.update(session, display)
        elif type(current_screen).__name__ == "PreLoadScr":
            common_events_allowed = False
            current_screen.update(session, display)
        elif type(current_screen).__name__ == "World":
            common_events_allowed = False
            current_screen.update(session, display, clock.get_fps())
        elif type(current_screen).__name__ == "MissionCompletedScr":
            common_events_allowed = False
            current_screen.update(display)

        for e in pygame.event.get(
            eventtype=(*commonEvents, *levelCode, *preloaderCode)
        ):
            if e.type == events.PLAY:
                # display a "Start a new game" confirmation box
                if (
                    ctypes.windll.user32.MessageBoxW(
                        0,
                        "Starting a new game will erase any progress that you have made. Continue?",
                        "Start a new game",
                        4,
                    )
                    == 6
                ):
                    # erase progress and start new game if user choose "Yes"
                    session.override_savefile()
                    current_screen = Intro()
                    pygame.event.set_allowed(
                        (
                            pygame.MOUSEBUTTONDOWN,
                            events.INTRODUCTION_DIALOGUE,
                            pygame.QUIT,
                            events.EXIT,
                        )
                    )
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if type(current_screen).__name__ == "Intro":
                    current_screen.flip()
                elif type(current_screen).__name__ == "Dialogue":
                    current_screen.next_line()
                    current_screen.update(display, session)

            elif e.type == events.INTRODUCTION_DIALOGUE:
                current_screen = Dialogue(session, (0, 1))
                pygame.event.set_allowed(
                    (
                        pygame.QUIT,
                        events.EXIT,
                        events.GO_TO_LV_SELECTION,
                        pygame.MOUSEBUTTONDOWN,
                    )
                )
            elif e.type == events.GO_TO_LV_SELECTION:
                current_screen = LvSelection()
                pygame.event.set_allowed(
                    (
                        pygame.QUIT,
                        events.PRELOAD_SCREEN,
                        *preloaderCode,
                        pygame.MOUSEBUTTONDOWN,
                    )
                )

            elif e.type == events.RESUME:
                current_screen = LvSelection()
                pygame.event.set_allowed(
                    (
                        pygame.QUIT,
                        events.PRELOAD_SCREEN,
                        *preloaderCode,
                        pygame.MOUSEBUTTONDOWN,
                    )
                )
            elif e.type == events.MISSION_COMPLETED:
                current_screen = MissionCompletedScr(session)
            elif e.type in preloaderCode:
                current_screen = PreLoadScr(session, Items(e.type))
                pygame.event.set_allowed(
                    (pygame.QUIT, pygame.MOUSEBUTTONDOWN, *levelCode)
                )
            elif e.type in levelCode:
                current_screen = World(session, Levels(e.type))

            elif e.type == pygame.QUIT or (
                e.type == pygame.KEYDOWN and e.key == pygame.KMOD_ALT | pygame.K_F4
            ):
                if (
                    ctypes.windll.user32.MessageBoxW(
                        0,
                        "Do you want to exit the game? Unsaved progress (if any) will be lost.",
                        "Exiting...",
                        0x04 | 0x30,
                    )
                    == 6
                ):
                    quit()

        pygame.display.flip()
        clock.tick(60)
