import random
from common.config import PlayerConfig
from session import Session
from pygame import transform
class TrailFx():
    def __init__(self, x, y, session: Session, speed) -> None:
        self.x = x
        self.dy = random.randint(-3, 3)
        self.y = y
        self.particle = session.TRAIL_PARTICLE_FX
        self.rect = self.particle.get_rect()
        self.rect.center = (self.x, self.y)
        self.scale = 1
        self.alpha = 255 * abs(speed) / PlayerConfig.MovingSpd
    def update(self):
        #self.rect.topleft = (self.x, self.y)
        #self.pivot_point = self.rect.center
        if self.alpha > 0:
            self.alpha -= 8
            self.scale -= 0.01
            if self.scale <= 0:
                self.scale = 0
            self.particle = transform.smoothscale(self.particle, (self.rect.width * self.scale, self.rect.height * self.scale))
            #self.rotated_rect = self.particle.get_rect()
            #self.rotated_rect.center = self.pivot_point
            self.particle.set_alpha(self.alpha)
            
            self.rect = self.particle.get_rect()
            self.rect.center = (self.x, self.y)
        self.rect.y += self.dy
    def render(self, display):
        self.update()
        display.blit(self.particle, (self.rect.x, self.rect.y))