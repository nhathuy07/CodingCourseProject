from random import randint, random
from common.config import BulletConfig
from session import Session
from pygame import transform, draw
from time import time


class PlayerBullet:
    def __init__(
        self,
        session: Session,
        x,
        y,
        dx=BulletConfig.Dx,
        dy = BulletConfig.Dy,
        gravity=BulletConfig.Gravity,
        damage=BulletConfig.Damage,
    ) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.gravity = gravity
        self.damage = damage
        self.images = session.projectile["PlayerBullet"]
        self.index = 0
        self.base_rect = self.images[0].get_rect()
        self.base_rect.center = (int(self.x), int(self.y))
        self.rect = self.base_rect
        self.animation_interval = 0.07
        self.last_animation_call = 0

        self.current_img = self.images[0]
        self.explosion_time = 0
        self.exploded = False
        # explosion effect settings
        self.fx_image = session.BULLET_EXPLOSION
        self.fx_rect = self.fx_image.get_rect()
        self.init_size = self.fx_image.get_width()
        self.fx_scale = 0.3
        self.alpha = 255

        self.init_coord = [self.x, self.y]

    def update(self, entities):

        if not self.exploded:

            self.current_img = self.images[self.index % len(self.images)]
            self.rect = self.base_rect
            self.rect.x += self.dx
            self.dy += self.gravity
            self.rect.y += self.dy
            if time() - self.last_animation_call >= self.animation_interval:
                self.index += 1
            for e in entities:
                if self.rect.colliderect(e.rect) and type(e).__name__ in ["Ground", "Enemy", "EnemyBoss"]:
                    self.explosion_time = time() + 0.01
            if time() >= self.explosion_time and self.explosion_time > 0:
                self.exploded = True
        elif self.alpha >= 0:

            self.rotation = randint(0, 360)
            self.fx_scale += 0.08
            self.alpha -= 11
            self.current_img = self.fx_image

            self.current_img.set_alpha(self.alpha)
            self.current_img = transform.smoothscale(
                self.current_img,
                (self.fx_scale * self.init_size, self.fx_scale * self.init_size),
            )
            self.fx_rect = self.current_img.get_rect()
            self.fx_rect.center = self.rect.center

        else:
            pass
        self.init_coord = self.rect.topleft

    def render(self, display, entities):
        # self.update(entities)
        if not self.exploded:
            display.blit(self.current_img, self.rect.topleft)
            draw.rect(display, (0, 255, 255), self.rect, 5)
        else:
            display.blit(self.current_img, self.fx_rect.topleft)
            draw.rect(display, (0, 255, 255), self.rect, 5)

class EnemyBullet(PlayerBullet):
    def __init__(
    self,
    session: Session,
    x,
    y,
    dx=BulletConfig.Dx,
    dy= BulletConfig.Dy,
    gravity=BulletConfig.Gravity,
    damage=BulletConfig.Damage,
    ) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.gravity = gravity
        self.damage = damage
        self.images = session.projectile["EnemyBullet"]
        self.index = 0
        self.base_rect = self.images[0].get_rect()
        self.base_rect.center = (int(self.x), int(self.y))
        self.rect = self.base_rect
        self.animation_interval = 0.07
        self.last_animation_call = 0

        self.current_img = self.images[0]
        self.explosion_time = 0
        self.exploded = False
        # explosion effect settings
        self.fx_image = session.ENEMY_BULLET_EXPLOSION
        self.fx_rect = self.fx_image.get_rect()
        self.init_size = self.fx_image.get_width()
        self.fx_scale = 0.3
        self.alpha = 255

        self.init_coord = [self.x, self.y]
    def update(self, entities):

        if not self.exploded:

            self.current_img = self.images[self.index % len(self.images)]
            self.rect = self.base_rect
            self.rect.x += self.dx
            self.dy += self.gravity
            self.rect.y += self.dy
            if time() - self.last_animation_call >= self.animation_interval:
                self.index += 1
            for e in entities:
                if self.rect.colliderect(e.rect) and type(e).__name__ in ["Ground", "Player"]:
                    self.explosion_time = time() + 0.01
            if time() >= self.explosion_time and self.explosion_time > 0:
                self.exploded = True
        elif self.alpha >= 0:

            self.rotation = randint(0, 360)
            self.fx_scale += 0.08
            self.alpha -= 11
            self.current_img = self.fx_image

            self.current_img.set_alpha(self.alpha)
            self.current_img = transform.smoothscale(
                self.current_img,
                (self.fx_scale * self.init_size, self.fx_scale * self.init_size),
            )
            self.fx_rect = self.current_img.get_rect()
            self.fx_rect.center = self.rect.center
    def render(self, display, entities):
        super().render(display, entities)