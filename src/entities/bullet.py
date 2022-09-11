from common.config import BulletConfig
from session import Session
from pygame import transform
from time import time
class PlayerBullet():
    def __init__(self, session: Session, x, y, dx = BulletConfig.Dx, gravity = BulletConfig.Gravity, damage = BulletConfig.Damage) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = 0
        self.gravity = gravity
        self.damage = damage
        self.images = session.projectile["PlayerBullet"]
        self.index = 0
        self.rect = self.images[0].get_rect()
        self.rect.center = (self.x, self.y)
        self.animation_interval = 0.07
        self.last_animation_call = 0
        
        # explosion effect settings
        self.last_fx_animation_call = 0
        self.fx_frame = 0
        self.fx_images = None
        self.fx_frame_interval = 0.05
        self.fx_scale = 0.3
        self.fx_alpha = 255
    def update(self):
        self.rect.x += self.dx
        self.dy += self.gravity
        self.rect.y += self.dy
        if time() - self.last_animation_call >= self.animation_interval:
            self.index += 1
        
    def render(self, display):
        self.update()
        display.blit(self.images[self.index % len(self.images)], self.rect.topleft)