from random import randint, random
from time import time
from common.config import DripstoneConfig
from common.extra_types import Projectiles
import entities
from session import Session
from pygame import transform
from visual_fx.dripstone_falling_fx import DripstoneFallingFx

#from world import World
class Dripstone():
    def __init__(self, session: Session, x, y, dy = DripstoneConfig.Dy, damage = DripstoneConfig.Damage, scale_min = DripstoneConfig.ScaleMin, scale_max = DripstoneConfig.ScaleMax, gravity = DripstoneConfig.Gravity, terminal_velocity = DripstoneConfig.TerminalVelocity, spawn_error = DripstoneConfig.SpawnError, dripstone_type = Projectiles.Dripstone) -> None:
        self.x = x
        self.y = y
        self.init_dy = dy
        self.gravity = gravity
        self.current_dy = self.init_dy
        self.damage = damage
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.scale = 1
        self.image = session.projectile["Dripstone"][0]
        #self.image = transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.init_coord = self.rect.topleft
        #self.spawn_error = randint(-spawn_error, spawn_error)s
        self.terminal_velocity = terminal_velocity
        self.falling = False
        self.falling_started = 0
        self.last_particle_spawn = 0
        self.falling_interval = 0.08
        self.waiting_time = randint(2, 4) / 10
        

    def update(self, session: Session, world):
        
        if not self.falling:
            if abs(self.rect.centerx - world.player.rect.centerx) < 40:
                self.falling = True
                self.falling_started = time()
        elif self.falling:
            if self.waiting_time - 0.15 < time() - self.falling_started <= self.waiting_time and time() - self.last_particle_spawn >= self.falling_interval:
                world.effects.append(DripstoneFallingFx(session, self))
                self.last_particle_spawn = time()
            elif time() - self.falling_started >= 0.43:
                if self.current_dy <= self.terminal_velocity:
                    self.current_dy += self.gravity
                else:
                    self.current_dy = self.terminal_velocity
                self.rect.y += self.current_dy
                self.check_collision_with_player(world.player)
        self.init_coord = self.rect.topleft
    def check_collision_with_player(self, player):
        if self.rect.colliderect(player.rect):
            # higher falling speed results in more severe damage
            player.inflict_damage(int(self.damage / self.terminal_velocity * self.current_dy), 0.5)
    def render(self, display):
        display.blit(self.image, self.rect.topleft)

