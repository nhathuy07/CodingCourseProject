from dis import dis
from pygame import image, transform, Rect, display
from common.paths import ASSETS_PATH, DATA_PATH

display.init()
display.set_mode()

WINDOW_SIZE = (1558, 961)
DISPLAY_SCALING = 0.7
TRANSISTION_SPEED = 10


def get_window_size(display_scaling=DISPLAY_SCALING):
    return WINDOW_SIZE[0] * display_scaling, WINDOW_SIZE[1] * display_scaling


FONT = (str(DATA_PATH / "fonts" / "Roboto-Bold.ttf"), int(32 * DISPLAY_SCALING))

CLICK_PROMPT = image.load(
    str(ASSETS_PATH / "icons" / "click-tap-svgrepo-com.png")
).convert_alpha()
CLICK_PROMPT = transform.smoothscale(
    CLICK_PROMPT, (CLICK_PROMPT.get_width() * 1.3, CLICK_PROMPT.get_height() * 1.3)
)

ITEM_PANE = image.load(str(ASSETS_PATH / "icons" / "itemPane.png"))
ITEM_PANE = transform.smoothscale(
    ITEM_PANE,
    (ITEM_PANE.get_width() * DISPLAY_SCALING, ITEM_PANE.get_height() * DISPLAY_SCALING),
)

DIALOG_DISP_AREA = Rect(20, 850 * DISPLAY_SCALING, get_window_size()[0] - 180, 100 - 20)
