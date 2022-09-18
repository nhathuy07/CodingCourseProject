from enum import Enum, auto
from pygame import USEREVENT



class Items(Enum):
    SHELL = USEREVENT + 120
    THRUSTER = USEREVENT + 121
    COMM_SYSTEM = USEREVENT + 122
    ENERGY_CORE = USEREVENT + 123



class Levels(Enum):
    SHELL = USEREVENT + 140
    THRUSTER = USEREVENT + 141
    COMM_SYSTEM = USEREVENT + 142
    ENERGY_CORE = USEREVENT + 143
    BOSS = USEREVENT + 144


class MenuOption(Enum):
    RESUME = 0
    RESTART_OR_START = 1
    ABOUT = 2
    HELP = 3


class Collectibles(Enum):
    GREEN = 10
    GREY = 11
    PURPLE = 12
    YELLOW = 13
    ENERGY_BAR = 14
    WEAPON_SUPERCHARGER = 15

Ores = (Collectibles.GREEN, Collectibles.GREY, Collectibles.PURPLE, Collectibles.YELLOW, Collectibles.ENERGY_BAR)

class Ground(Enum):
    # Base = -1
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
    OuterSpace = 3


class Mobs(Enum):
    LvOne = 20
    LvTwo = 21
    LvThree = 22


class Projectiles(Enum):
    # EnemyBullet = 30
    Dripstone = 31
    EnemyBullet = 32
    PlayerBullet = 33
    Meteorite = 34


class Liquid(Enum):
    Acid = 40
    Lava = 41



# States
class PlayerState(Enum):
    Attacked = 100
    Idle = 101
    Moving = 102
    Shooting = 103
    AttackedWhileMoving = 104
    Destroyed = 105


class Mobs(Enum):
    Type1 = 0
    Type2 = 1
    Type3 = 2


class MobState(Enum):
    Idle = "idle"
    Attacking = "attacking"
    Hurt = "hurt"

class BossState(Enum):
    Idle = "idle"
    Growling = "growling"
    SpittingBullet = "spitting_bullet"
    DroppingBomb = "dropping_bomb"

class OptionalFeature(Enum):
    ReducedSight = "ReducedSight"
