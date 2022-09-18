from common import extra_types
from session import Session


class Liquid:
    def __init__(self, session: Session, x, y, liquid_type: extra_types.Liquid) -> None:
        self.init_coord = (x, y)
        self.x = x
        self.y = y
        self.image = session.liquid_texture[liquid_type.name]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
