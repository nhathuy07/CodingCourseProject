from common.config import DISPLAY_SCALING
from common.types import Collectibles
from session import Session


class Collectible:
    def __init__(self, collectible_type: Collectibles, session: Session, x, y, og_position = False) -> None:
        self.og_position = False
        self.init_coord = (x, y)
        self.x = x
        self.y = y
        self.collectible_type = collectible_type
        self.base = session.collectibles[collectible_type.name]["Base"]
        self.glowFx = session.collectibles[collectible_type.name]["GlowFx"]

        self.rect = self.base.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.size = (60 * DISPLAY_SCALING, 60 * DISPLAY_SCALING)

        self.glowFxRect = self.glowFx.get_rect()
        self.glowFxRect.center = self.rect.center

        self.alpha = 255
        self.alpha_changing_direction = 0  # 0 = up, 1 = down

        self.current_fx = self.glowFx.copy()

    def update(self, display):
        if self.glowFx != None:
            self.current_fx = self.glowFx.copy()
            if self.alpha < 160:
                self.alpha_changing_direction = 0
            elif self.alpha > 255:
                self.alpha_changing_direction = 1

            if self.alpha_changing_direction == 0:
                self.alpha += 2
            else:
                self.alpha -= 2

            self.current_fx.set_alpha(self.alpha)
            self.glowFxRect.center = self.rect.center

    def render(self, display):
        self.update(display)
        if self.glowFx != None:
            display.blit(self.current_fx, self.glowFxRect.topleft)

        display.blit(self.base, self.rect.topleft)
