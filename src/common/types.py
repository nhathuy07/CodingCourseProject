from enum import Enum, auto
from pygame import USEREVENT


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

class Ground(Enum):
    Base = -1
    NoFace = 0
    RightFace = 1
    LeftFace = 2
    UpFace = 3
    RightUpFace = 4
    LeftUpFace = 5
    DownFace = 6
    RightDownFace = 7
    LeftDownFace = 8
    FacingTopBottom = 9
    FacingTopRightBottom = 10
    FacingTopLeftBottom = 11
    FacingLeftRight = 12
    FacingTopLeftRight = 13
    FacingBottomLeftRight = 14
    FacingAll = 15

class Scheme(Enum):
    BlueCave = 0
    LavaCave = 1
    DarkCave = 2

class Mobs(Enum):
    LvOne = 20
    LvTwo = 21
    LvThree = 22

class Projectiles(Enum):
    EnemyBullet = 30
    Dripstone = 31