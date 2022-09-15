from random import randint

from common.config import DISPLAY_SCALING
#from entities.dripstone import Dripstone

class DripstoneFallingFx():
    def __init__(self, session, dripstone) -> None:
        self.x = dripstone.rect.centerx
        self.y = dripstone.rect.y - randint(-200, 0)
        self.image = session.DRIPSTONE_FALLING
        self.error = randint(int(-30 * DISPLAY_SCALING), int(30 * DISPLAY_SCALING))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x + self.error, self.y)
        self.dy = 15
        self.alpha = 100
    def update(self):
        self.rect.y += self.dy
    def render(self, display):
        self.update()
        display.blit(self.image, self.rect.topleft)