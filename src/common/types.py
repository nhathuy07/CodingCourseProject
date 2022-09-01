from enum import Enum
from pygame import USEREVENT


class GameSection(Enum):
    INTRO = -1
    MAIN_MENU = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4


class Items(Enum):
    SHELL = USEREVENT + 20
    THRUSTER = USEREVENT + 21
    COMM_SYSTEM = USEREVENT + 22
    ENERGY_CORE = USEREVENT + 23


class Levels(Enum):
    SHELL = USEREVENT + 40
    THRUSTER = USEREVENT + 41
    COMM_SYSTEM = USEREVENT + 42
    ENERGY_CORE = USEREVENT + 43
    BOSS = USEREVENT + 44


class MenuOption(Enum):
    RESUME = 0
    RESTART_OR_START = 1
    ABOUT = 2
    HELP = 3

class Collectibles(Enum):
    GREEN = -1
    GREY = -2
    PURPLE = -3
    YELLOW = -4
    ENERGY_BAR = -5