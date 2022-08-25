from pygame import image, transform, Rect
from common.paths import ASSETS_PATH, DATA_PATH


WINDOW_SIZE = (1558, 961)
DISPLAY_SCALING = 0.7
TRANSISTION_SPEED = 10

def get_window_size(display_scaling = DISPLAY_SCALING):
    return WINDOW_SIZE[0] * display_scaling, WINDOW_SIZE[1] * display_scaling

FONT = (str(DATA_PATH / "fonts" / "Roboto-Bold.ttf"), int(32 * DISPLAY_SCALING))

CLICK_PROMPT = image.load(str(ASSETS_PATH / "icons" / "click-tap-svgrepo-com.png"))
CLICK_PROMPT = transform.smoothscale(CLICK_PROMPT, (CLICK_PROMPT.get_width() * 1.3, CLICK_PROMPT.get_height() * 1.3))

DIALOG_DISP_AREA = Rect(20, get_window_size()[1] - 200, get_window_size()[0] - 40, 200 - 20)