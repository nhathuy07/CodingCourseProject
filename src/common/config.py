from dataclasses import dataclass
from pygame import Rect, display
from common.paths import DATA_PATH

display.init()
display.set_mode()

WINDOW_SIZE = (1558, 961)
DISPLAY_SCALING = 0.8
TRANSISTION_SPEED = 13


def get_window_size(display_scaling=DISPLAY_SCALING):
    return WINDOW_SIZE[0] * display_scaling, WINDOW_SIZE[1] * display_scaling


FONT = (str(DATA_PATH / "fonts" / "Roboto-Bold.ttf"), int(32 * DISPLAY_SCALING))
FONT2 = (str(DATA_PATH / "fonts" / "Inter-Bold.ttf"), int(32 * DISPLAY_SCALING))


DIALOG_DISP_AREA = Rect(20, 850 * DISPLAY_SCALING, get_window_size()[0] - 180, 100 - 20)


@dataclass
class PlayerConfig:
    InitX = 80
    InitY = 80
    MovingSpd = 10
    JumpingSpd = 22
    Gravity = 0.75
    Acceleration = 0.7
    Deceleration = 0.55
    HP = 100
    SoftEdge = 300
    PerkDuration = 22
    WeaponCooldown = 0.2


@dataclass
class BulletConfig:
    Dx = 35
    Dy = 0
    Gravity = 0.2
    Damage = 20


@dataclass
class EnemyConfig:
    Dx = 7
    Dy = 6
    Damage = 6
    Hp = 20
    LocateTargetDelay = 0.6
    LocateTargetError = 10
    WeaponCooldown = 0.4


@dataclass
class EnemyType2Config:
    Dx = 9
    Dy = 8
    Damage = 10
    Hp = 35
    LocateTargetDelay = 0.25
    LocateTargetError = 6
    WeaponCooldown = 0.2


@dataclass
class EnemyType3Config:
    Dx =  8
    Dy = 5
    Damage = 12
    Hp = 40
    LocateTargetDelay = 0.4
    LocateTargetError = 40
    WeaponCooldown = 0.18


@dataclass
class BossConfig:
    Dx = 9.5
    Dy = 8
    Damage = 25
    SimultaneousBulletSpawn = (7, 13)
    SimultaneousMeteoriteSpawn = 7
    #InstakillPosibilities = 0.1
    GrowlKnockbackDistance = 70
    Hp = 230
    #Hp = 20 #<== for debugging purposes only
@dataclass
class DripstoneConfig:
    Dy = 16
    Damage = 30
    ScaleMin = 0.3
    ScaleMax = 1
    SpawnError = 100
    SpawnQuantity = 5
    Gravity = 0.25
    TerminalVelocity = 28