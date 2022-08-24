from lib2to3.pytree import convert
from pygame import image, display
from pygame import surface, transform
from common import config

display.init()
display.set_mode()

def load_img(path, scaling = config.DISPLAY_SCALING):
    img = image.load(path).convert_alpha()
    img = transform.smoothscale(img, (img.get_width() * scaling, img.get_height() * scaling))
    return img