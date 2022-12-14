from pygame import image, display, Rect
from pygame import surface, transform
from common import config

display.init()
display.set_mode()


def load_img(path, scaling=config.DISPLAY_SCALING):
    img = image.load(path).convert_alpha()
    img = transform.smoothscale(
        img, (img.get_width() * scaling, img.get_height() * scaling)
    )
    return img


def image_scale(surface: surface.Surface, scale: float):
    return transform.smoothscale(
        surface, (surface.get_width() * scale, surface.get_height() * scale)
    )


def drawText(surface, text, color, rect, font, aa=True, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
