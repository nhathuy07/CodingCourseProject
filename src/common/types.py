from enum import Enum

class GameSection(Enum):
    INTRO = -1
    MAIN_MENU = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4

class Items(Enum):
    SHELL = 0
    THRUSTER = 1
    COMM_SYSTEM = 2
    ENERGY_CORE = 3

class MenuOption(Enum):
    RESUME = 0
    RESTART_OR_START = 1
    ABOUT = 2
    HELP = 3