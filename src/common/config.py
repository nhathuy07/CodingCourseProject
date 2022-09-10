from dataclasses import dataclass
from dis import dis
from pygame import image, transform, Rect, display
from common.paths import ASSETS_PATH, DATA_PATH

display.init()
display.set_mode()

WINDOW_SIZE = (1558, 961)
DISPLAY_SCALING = 0.8
TRANSISTION_SPEED = 10


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
