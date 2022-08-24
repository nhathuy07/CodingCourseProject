WINDOW_SIZE = (1558, 961)
DISPLAY_SCALING = 0.7
TRANSISTION_SPEED = 10

def get_window_size(display_scaling = DISPLAY_SCALING):
    return WINDOW_SIZE[0] * display_scaling, WINDOW_SIZE[1] * display_scaling