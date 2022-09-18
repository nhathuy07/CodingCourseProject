from common import extra_types

from session import Session


class Ground:
    def __init__(
        self, session: Session, variation: extra_types.Ground, scheme: extra_types.Scheme, x, y
    ):
        self.init_coord = (x, y)
        self.image = session.ground_texture[scheme.value][variation.name]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)

    def render(self, display):
        display.blit(self.image, self.rect.topleft)
