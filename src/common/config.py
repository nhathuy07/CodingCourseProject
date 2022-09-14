from dataclasses import dataclass
from dis import dis
from pygame import image, transform, Rect, display
from common.paths import ASSETS_PATH, DATA_PATH

display.init()
display.set_mode()

WINDOW_SIZE = (1558, 961)
DISPLAY_SCALING = 0.8
TRANSISTION_SPEED = 18


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


@dataclass
class BulletConfig:
    Dx = 35
    Gravity = 0.2
    Damage = 20


@dataclass
class EnemyConfig:
    Dx = 7
    Dy = 6
    Damage = 6
    Hp = 25
    LocateTargetDelay = 0.6
    LocateTargetError = 10
    WeaponCooldown = 0.4


@dataclass
class EnemyType2Config:
    Dx = 13.5
    Dy = 16.5
    Damage = 10
    Hp = 40
    LocateTargetDelay = 0.25
    LocateTargetError = 6
    WeaponCooldown = 0.2


@dataclass
class EnemyType3Config:
    Dx = 32
    Dy = 14
    Damage = 15
    Hp = 45
    LocateTargetDelay = 0.3
    LocateTargetError = 5
    WeaponCooldown = 0.18


@dataclass
class BossConfig:
    Dx = 28
    Dy = 12
    Damage = 25
    SimultaneousBulletSpawn = (10, 20)
    SimultaneousMeteoriteSpawn = (5, 7)
    InstakillPosibilities = 0.1
    GrowlKnockbackDistance = 20
